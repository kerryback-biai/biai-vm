#!/bin/bash
# Entrypoint for Koyeb container
# Sets up student accounts and starts web terminal

set -e

# Set API key from environment
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_API_KEY\"" > /etc/profile.d/anthropic.sh
    chmod 644 /etc/profile.d/anthropic.sh
fi

# Create student accounts from shared database
# Falls back to STUDENTS env var if DATABASE_URL is not set
STUDENT_LIST=""
if [ -n "$DATABASE_URL" ]; then
    STUDENT_LIST=$(python3 /fetch-students.py 2>/dev/null || true)
elif [ -n "$STUDENTS" ]; then
    # Legacy format: "user1:pass1,user2:pass2"
    STUDENT_LIST=$(echo "$STUDENTS" | tr ',' '\n')
fi

if [ -n "$STUDENT_LIST" ]; then
    while IFS=: read -r USERNAME PASSWORD; do
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
    done <<< "$STUDENT_LIST"
fi

# Login banner displayed after authentication
cat > /etc/motd << 'MOTD'

  ╔══════════════════════════════════════════════════╗
  ║     From BI to AI — Data Agent Workshop          ║
  ║     Meridian Corp Executive Program              ║
  ╚══════════════════════════════════════════════════╝

  To get started:
    cd workspace
    claude

  Your exercise files are in ~/workspace/.
  Type 'quit' or Ctrl-C to exit Claude Code.

MOTD

# Pre-login banner displayed on the ttyd login screen
cat > /etc/issue.net << 'ISSUE'

  Welcome to the BI-to-AI Workshop Server
  Log in with the credentials provided by your instructor.

ISSUE
cp /etc/issue.net /etc/issue

# Start ttyd web terminal on port 8000
exec ttyd --port 8000 --writable -t titleFixed="BI to AI Workshop" login
