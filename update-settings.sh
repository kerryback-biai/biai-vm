#!/bin/bash
# Update Claude settings.json for all users
source /etc/biai.env

for user in $(cut -d: -f1 /etc/biai-ports); do
    mkdir -p "/home/$user/.claude"
    cat > "/home/$user/.claude/settings.json" << EOF
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
EOF
    chown -R "$user" "/home/$user/.claude"
    echo "Updated $user"
done
