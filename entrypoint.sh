#!/bin/bash
# Entrypoint for Koyeb container
# Sets up student accounts and starts web terminal

set -e

# Set API key from environment
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_API_KEY\"" > /etc/profile.d/anthropic.sh
    chmod 644 /etc/profile.d/anthropic.sh
fi

# Create student accounts from STUDENTS env var
# Format: "user1:pass1,user2:pass2"
if [ -n "$STUDENTS" ]; then
    IFS=',' read -ra PAIRS <<< "$STUDENTS"
    for pair in "${PAIRS[@]}"; do
        IFS=':' read -r USERNAME PASSWORD <<< "$pair"
        [ -z "$USERNAME" ] && continue

        if ! id "$USERNAME" &>/dev/null; then
            useradd -m -s /bin/bash "$USERNAME"
            echo "$USERNAME:$PASSWORD" | chpasswd

            WORKSPACE="/home/$USERNAME/workspace"
            mkdir -p "$WORKSPACE"

            # Copy exercise templates
            cp -r /shared/templates/* "$WORKSPACE/" 2>/dev/null || true

            # Symlink to shared data
            ln -sf /shared/data "$WORKSPACE/data"

            # Claude Code settings
            mkdir -p "/home/$USERNAME/.claude/skills"
            cat > "/home/$USERNAME/.claude/settings.json" << 'SETTINGS'
{
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
    ]
  }
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

            chown -R "$USERNAME:$USERNAME" "/home/$USERNAME"
            echo "Created student: $USERNAME"
        fi
    done
fi

# Start ttyd web terminal on port 8000
# --writable allows input; login prompt lets students authenticate
exec ttyd --port 8000 --writable login
