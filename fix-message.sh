#!/bin/bash
for user in $(cut -d: -f1 /etc/biai-ports); do
    sed -i 's/To enter Claude Code, type "claude" and hit ENTER./To enter Claude Code, type "claude" (without quotes) and hit ENTER./' /home/$user/.bashrc
    echo "Fixed $user"
done
