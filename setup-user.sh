#!/bin/bash
# Set up workspace and services for an existing Linux user
# Usage: sudo bash setup-user.sh <username>
# The user must already exist (created with useradd + passwd)
set -e

if [ -z "$1" ]; then
    echo "Usage: sudo bash setup-user.sh <username>"
    exit 1
fi

USERNAME="$1"

if ! id "$USERNAME" &>/dev/null; then
    echo "Error: user '$USERNAME' does not exist. Create with:"
    echo "  useradd -m -s /bin/bash $USERNAME"
    echo "  passwd $USERNAME"
    exit 1
fi

# Load API key
source /etc/biai.env 2>/dev/null || true

WORKSPACE="/home/$USERNAME/workspace"
mkdir -p "$WORKSPACE"

# Copy exercise templates (skip if already populated)
if [ ! -f "$WORKSPACE/ex1_hello_agent.py" ]; then
    cp -r /shared/templates/* "$WORKSPACE/" 2>/dev/null || true
fi

# Symlink to shared data
ln -sf /shared/data "$WORKSPACE/data"

# Claude Code settings
mkdir -p "/home/$USERNAME/.claude/skills"
cat > "/home/$USERNAME/.claude/settings.json" << SETTINGS
{
  "theme": "light",
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

# Add API key and auto-launch claude in .bashrc (idempotent)
if ! grep -q "ANTHROPIC_API_KEY" "/home/$USERNAME/.bashrc" 2>/dev/null; then
    cat >> "/home/$USERNAME/.bashrc" << BASHRC

export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"

# Auto-launch Claude Code
if [ -t 1 ] && [ -z "\$CLAUDE_LAUNCHED" ]; then
    export CLAUDE_LAUNCHED=1
    cd ~/workspace
    exec claude
fi
BASHRC
fi

chown -R "$USERNAME" "/home/$USERNAME"

# Complete Claude Code first-run setup non-interactively
# This accepts the API key so students never see the approval prompt
su - "$USERNAME" -c "cd ~/workspace && ANTHROPIC_API_KEY='${ANTHROPIC_API_KEY}' claude -p 'hello' --max-turns 1" > /dev/null 2>&1 || true

# Assign ports: hash username to a stable port pair
# Use /etc/biai-ports to track assignments
PORTS_FILE="/etc/biai-ports"
touch "$PORTS_FILE"

if grep -q "^$USERNAME:" "$PORTS_FILE"; then
    TTYD_PORT=$(grep "^$USERNAME:" "$PORTS_FILE" | cut -d: -f2)
    FB_PORT=$(grep "^$USERNAME:" "$PORTS_FILE" | cut -d: -f3)
    TERM_PORT=$(grep "^$USERNAME:" "$PORTS_FILE" | cut -d: -f4)
    # Backfill term port if missing (3-field legacy format)
    if [ -z "$TERM_PORT" ]; then
        TERM_PORT=$((TTYD_PORT + 2000))
        sed -i "s/^$USERNAME:$TTYD_PORT:$FB_PORT$/$USERNAME:$TTYD_PORT:$FB_PORT:$TERM_PORT/" "$PORTS_FILE"
    fi
else
    # Find next available port pair
    LAST_TTYD=$(awk -F: '{print $2}' "$PORTS_FILE" | sort -n | tail -1)
    TTYD_PORT=${LAST_TTYD:-9000}
    TTYD_PORT=$((TTYD_PORT + 1))
    FB_PORT=$((TTYD_PORT + 1000))
    TERM_PORT=$((TTYD_PORT + 2000))
    echo "$USERNAME:$TTYD_PORT:$FB_PORT:$TERM_PORT" >> "$PORTS_FILE"
fi

# ttyd service
cat > "/etc/systemd/system/ttyd-${USERNAME}.service" << SYSTEMD
[Unit]
Description=ttyd terminal for $USERNAME
After=network.target

[Service]
Type=simple
User=$USERNAME
Environment=ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
WorkingDirectory=/home/$USERNAME/workspace
ExecStart=/usr/local/bin/ttyd --port $TTYD_PORT --writable --base-path /$USERNAME/ -t titleFixed="AI Lab" bash -l
Restart=on-failure

[Install]
WantedBy=multi-user.target
SYSTEMD

# filebrowser service
cat > "/etc/systemd/system/filebrowser-${USERNAME}.service" << SYSTEMD
[Unit]
Description=Filebrowser for $USERNAME
After=network.target

[Service]
Type=simple
User=$USERNAME
ExecStart=/usr/local/bin/filebrowser --root /home/$USERNAME/workspace --address 127.0.0.1 --port $FB_PORT --baseURL /$USERNAME/files --database /home/$USERNAME/.filebrowser.db
Restart=on-failure

[Install]
WantedBy=multi-user.target
SYSTEMD

# Plain terminal service (no claude auto-launch)
cat > "/etc/systemd/system/ttyd-term-${USERNAME}.service" << SYSTEMD
[Unit]
Description=Plain terminal for $USERNAME
After=network.target

[Service]
Type=simple
User=$USERNAME
Environment=ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
Environment=CLAUDE_LAUNCHED=1
WorkingDirectory=/home/$USERNAME/workspace
ExecStart=/usr/local/bin/ttyd --port $TERM_PORT --writable --base-path /$USERNAME/term/ -t titleFixed="Terminal" bash -l
Restart=on-failure

[Install]
WantedBy=multi-user.target
SYSTEMD

# Initialize FileBrowser database with proxy auth (no login required)
FB_DB="/home/$USERNAME/.filebrowser.db"
if [ ! -f "$FB_DB" ]; then
    filebrowser config init --auth.method=proxy --auth.header=X-FB-User --database "$FB_DB"
    filebrowser users add admin adminpassword123 --perm.admin=false --database "$FB_DB"
fi
chown "$USERNAME" "$FB_DB"

systemctl daemon-reload
systemctl enable --now "ttyd-${USERNAME}.service"
systemctl enable --now "filebrowser-${USERNAME}.service"
systemctl enable --now "ttyd-term-${USERNAME}.service"

# Regenerate nginx config
bash /opt/biai-vm/generate-nginx.sh

echo "Done: $USERNAME (claude=:$TTYD_PORT, files=:$FB_PORT, term=:$TERM_PORT)"
echo "URL: https://ai-lab.rice-business.org/$USERNAME/"
