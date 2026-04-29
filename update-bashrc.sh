#!/bin/bash
# Update .bashrc for all users: clean startup message, no auto-launch
source /etc/biai.env

for user in $(cut -d: -f1 /etc/biai-ports); do
    # Remove old blocks
    sed -i '/# Welcome banner/,/^fi$/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/# Auto-launch Claude/,/^fi$/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/# Show startup message/,/^fi$/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/ANTHROPIC_API_KEY/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/ANTHROPIC_BASE_URL/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/CLAUDE_LAUNCHED/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/cd ~\/workspace/d' /home/$user/.bashrc 2>/dev/null
    sed -i '/exec claude/d' /home/$user/.bashrc 2>/dev/null
    # Remove blank lines at end of file
    sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' /home/$user/.bashrc 2>/dev/null

    # Add clean block
    cat >> /home/$user/.bashrc << EOF

export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"

# Show startup message
if [ -t 1 ] && [ -z "\$CLAUDE_LAUNCHED" ]; then
    export CLAUDE_LAUNCHED=1
    cd ~/workspace
    echo 'To enter Claude Code, type "claude" and hit ENTER.'
fi
EOF
    chown "$user" "/home/$user/.bashrc"
    echo "Updated $user"
done
