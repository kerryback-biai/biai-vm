#!/bin/bash
# Provision student accounts from Postgres database
# Usage: sudo bash provision-students.sh
# Requires DATABASE_URL and ANTHROPIC_API_KEY in /etc/biai.env
set -e

set -a
source /etc/biai.env
set +a

echo "=== Provisioning student accounts ==="

# Fetch students from database
STUDENT_LIST=$(python3 /opt/biai-vm/fetch-students.py 2>&1)
if [ -z "$STUDENT_LIST" ]; then
    echo "No students found in database."
    exit 0
fi

TTYD_PORT=9001
FB_PORT=8001
NGINX_LOCATIONS=""

while IFS=: read -r USERNAME PASSWORD; do
    [ -z "$USERNAME" ] && continue

    if id "$USERNAME" &>/dev/null; then
        echo "  EXISTS: $USERNAME (ttyd=$TTYD_PORT, files=$FB_PORT)"
    else
        # Create Linux user (-N skips creating a group with the same name)
        useradd -m -s /bin/bash -N "$USERNAME"
        echo "$USERNAME:$PASSWORD" | chpasswd

        WORKSPACE="/home/$USERNAME/workspace"
        mkdir -p "$WORKSPACE"

        # Copy exercise templates
        cp -r /shared/templates/* "$WORKSPACE/" 2>/dev/null || true

        # Symlink to shared data
        ln -sf /shared/data "$WORKSPACE/data"

        # Claude Code settings
        mkdir -p "/home/$USERNAME/.claude/skills"

        # Global preferences (theme, etc.) — stored in ~/.claude.json
        cat > "/home/$USERNAME/.claude.json" << 'CLAUDEJSON'
{
  "theme": "light"
}
CLAUDEJSON

        cat > "/home/$USERNAME/.claude/settings.json" << SETTINGS
{
  "env": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
  },
  "permissions": {
    "allow": [
      "Bash(python*)",
      "Bash(pip*)",
      "Bash(duckdb*)",
      "Bash(ls*)",
      "Bash(cat*)",
      "Bash(head*)",
      "Bash(node*)",
      "Bash(pandoc*)",
      "Bash(libreoffice*)",
      "Bash(soffice*)",
      "Bash(pdftoppm*)",
      "Bash(cp*)",
      "Bash(mv*)",
      "Bash(mkdir*)",
      "Bash(unzip*)",
      "Bash(zip*)",
      "Read",
      "Write",
      "Edit"
    ],
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
SETTINGS

        # Copy skills
        cp -r /shared/skills/* "/home/$USERNAME/.claude/skills/" 2>/dev/null || true

        # Project instructions
        cat > "$WORKSPACE/CLAUDE.md" << 'CLAUDEMD'
# AI Data Agent Workshop

You are helping a student build a data agent from scratch.

## Environment
- Data files are in `./data/` (symlink to /shared/data)
- Use DuckDB to query parquet files: `duckdb.sql("SELECT * FROM read_parquet('data/file.parquet')")`
- The Anthropic API key is already set in the environment
- Use `anthropic` Python package for API calls

## Guidelines
- Help the student understand each piece of the agent loop
- Don't write the entire solution at once — build incrementally
- Explain what each part does as you go
- When the student gets stuck, give hints rather than complete solutions
CLAUDEMD

        # Set API key and auto-launch claude in .bashrc
        cat >> "/home/$USERNAME/.bashrc" << BASHRC

export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
export ANTHROPIC_BASE_URL="http://localhost:8080/proxy/$USERNAME"

# Auto-launch Claude Code in terminal
if [ -t 1 ] && [ -z "\$CLAUDE_LAUNCHED" ]; then
    export CLAUDE_LAUNCHED=1
    cd ~/workspace
    exec claude
fi
BASHRC

        chown -R "$USERNAME:$USERNAME" "/home/$USERNAME"

        # Complete Claude Code first-run setup non-interactively
        # This accepts the API key so students never see the approval prompt
        su - "$USERNAME" -c "cd ~/workspace && ANTHROPIC_API_KEY='${ANTHROPIC_API_KEY}' claude -p 'hello' --max-turns 1" > /dev/null 2>&1 || true

        echo "  CREATED: $USERNAME (ttyd=$TTYD_PORT, files=$FB_PORT)"
    fi

    # --- ttyd service (terminal with Claude Code) ---
    cat > "/etc/systemd/system/ttyd-${USERNAME}.service" << SYSTEMD
[Unit]
Description=ttyd terminal for $USERNAME
After=network.target

[Service]
Type=simple
User=$USERNAME
Environment=ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
WorkingDirectory=/home/$USERNAME/workspace
ExecStart=/usr/local/bin/ttyd --port $TTYD_PORT --writable --base-path /$USERNAME/ -t titleFixed="AI+Code Lab" -t 'theme={"background":"#ffffff","foreground":"#000000","cursor":"#000000","selectionBackground":"#b0c4de"}' bash -l
Restart=on-failure

[Install]
WantedBy=multi-user.target
SYSTEMD

    # --- filebrowser service ---
    FB_DB="/home/$USERNAME/.filebrowser.db"
    cat > "/etc/systemd/system/filebrowser-${USERNAME}.service" << SYSTEMD
[Unit]
Description=Filebrowser for $USERNAME
After=network.target

[Service]
Type=simple
User=$USERNAME
ExecStart=/usr/local/bin/filebrowser --noauth --root /home/$USERNAME/workspace --address 127.0.0.1 --port $FB_PORT --baseurl /$USERNAME/files --database $FB_DB
Restart=on-failure

[Install]
WantedBy=multi-user.target
SYSTEMD

    systemctl daemon-reload
    systemctl enable --now "ttyd-${USERNAME}.service"
    systemctl enable --now "filebrowser-${USERNAME}.service"

    # Collect nginx location blocks
    NGINX_LOCATIONS="$NGINX_LOCATIONS
    # $USERNAME — terminal
    location /$USERNAME/ {
        proxy_pass http://127.0.0.1:$TTYD_PORT;
        proxy_set_header Host \$host;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_http_version 1.1;

        # Inject header banner
        proxy_set_header Accept-Encoding \"\";
        sub_filter '</head>' '<style>#biai-banner{background:#1e1e2e;color:#cdd6f4;text-align:center;padding:6px 0;font-family:system-ui,sans-serif;font-size:13px;letter-spacing:0.3px;position:fixed;top:0;left:0;right:0;z-index:99999;line-height:1.4}#biai-banner strong{color:#89b4fa}</style></head>';
        sub_filter '</body>' '<div id=\"biai-banner\"><strong>AI+Code Lab</strong> &ensp;|&ensp; Rice Business Executive Education &ensp;|&ensp; Professor Kerry Back</div></body>';
        sub_filter_once on;
        sub_filter_types text/html;
    }

    # $USERNAME — file browser
    location /$USERNAME/files/ {
        proxy_pass http://127.0.0.1:$FB_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
    }"

    TTYD_PORT=$((TTYD_PORT + 1))
    FB_PORT=$((FB_PORT + 1))

done <<< "$STUDENT_LIST"

# Write nginx config
echo ""
echo "=== Configuring nginx ==="
cat > /etc/nginx/sites-available/biai-vm << NGINX
server {
    listen 80;
    server_name vm.kerryback.com _;
    client_max_body_size 50M;

    location = / {
        default_type text/html;
        return 200 '<html><head><title>BI to AI Workshop</title>
<style>
body{font-family:system-ui;max-width:600px;margin:80px auto;padding:0 20px;color:#333}
h1{margin-bottom:0.2em}
h2{color:#666;font-weight:normal;font-size:1.1em;margin-top:0}
code{background:#f0f0f0;padding:2px 6px;border-radius:3px}
.links{margin-top:2em}
.links a{display:inline-block;margin-right:1.5em;color:#0066cc}
</style></head>
<body>
<h1>AI+Code Lab</h1>
<h2>Rice Business Executive Education &mdash; Professor Kerry Back</h2>
<p>Access your workspace using the URL provided by your instructor.</p>
</body></html>';
    }
$NGINX_LOCATIONS
}
NGINX

# Enable site, remove default
ln -sf /etc/nginx/sites-available/biai-vm /etc/nginx/sites-enabled/biai-vm
rm -f /etc/nginx/sites-enabled/default

nginx -t && systemctl reload nginx
echo "Nginx configured."

echo ""
echo "=== Done ==="
echo "Each student gets two URLs:"
echo "  Terminal:  https://vm.kerryback.com/<username>/"
echo "  Files:     https://vm.kerryback.com/<username>/files/"
