#!/bin/bash
# Install git for all existing users on the AI-Lab server
# Run as root: sudo bash install-git-users.sh
set -e

PORTS_FILE="/etc/biai-ports"

if [ ! -f "$PORTS_FILE" ]; then
    echo "Error: $PORTS_FILE not found"
    exit 1
fi

while IFS=: read -r user _; do
    ws="/home/$user/workspace"
    settings="/home/$user/.claude/settings.json"

    # 1. Add git permission to Claude Code settings
    if [ -f "$settings" ] && ! grep -q '"Bash(git\*)"' "$settings"; then
        sed -i 's/"Bash(zip\*)"/"Bash(git*)",\n      "Bash(zip*)"/' "$settings"
        echo "[$user] Added git permission to settings.json"
    fi

    # 2. Initialize git repo in workspace
    if [ -d "$ws" ] && [ ! -d "$ws/.git" ]; then
        su - "$user" -c "cd ~/workspace && git init && git config user.name '$user' && git config user.email '$user@ai-lab'"
        cat > "$ws/.gitignore" << 'EOF'
data
__pycache__/
*.pyc
.env
EOF
        chown "$user" "$ws/.gitignore"
        echo "[$user] Initialized git repo"
    fi
done < "$PORTS_FILE"

echo "Done. All users updated."
