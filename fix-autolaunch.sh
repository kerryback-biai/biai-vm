#!/bin/bash
for user in $(cut -d: -f1 /etc/biai-ports); do
    sed -i "s/echo 'To enter Claude Code, type \"claude\" (without quotes) and hit ENTER.'/exec claude/" /home/$user/.bashrc
    echo "Fixed $user"
done
