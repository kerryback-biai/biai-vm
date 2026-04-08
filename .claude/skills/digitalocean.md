---
name: digitalocean
description: "Manage the biai-vm DigitalOcean droplet. Use this skill for server management: SSH commands, service status, droplet power operations, deploying code, checking logs, managing nginx, and student provisioning."
---

# DigitalOcean Server Management — biai-vm

## Server Details

- **Droplet Name**: biai-vm
- **Droplet ID**: 562286347
- **IP Address**: 157.245.133.86
- **Region**: nyc1
- **Size**: s-2vcpu-4gb-120gb-intel
- **OS**: Ubuntu 24.04 LTS
- **Domain**: vm.kerryback.com
- **SSH Access**: `ssh root@157.245.133.86`

## CLI Setup

doctl is installed via winget. Always set the PATH before using it:

```bash
export PATH="$PATH:/c/Users/kerry/AppData/Local/Microsoft/WinGet/Packages/DigitalOcean.Doctl_Microsoft.Winget.Source_8wekyb3d8bbwe"
```

Authentication token is stored in doctl's config (authenticated via `doctl auth init`).

## Common Operations

### Droplet Management

```bash
# Check droplet status
doctl compute droplet get 562286347 --format Name,PublicIPv4,Status,SizeSlug

# Power cycle (reboot)
doctl compute droplet-action reboot 562286347

# Power off
doctl compute droplet-action power-off 562286347

# Power on
doctl compute droplet-action power-on 562286347

# Resize droplet (must be powered off first for CPU changes)
doctl compute droplet-action resize 562286347 --size <size-slug>

# List available sizes
doctl compute size list

# Take a snapshot
doctl compute droplet-action snapshot 562286347 --snapshot-name "biai-vm-$(date +%Y%m%d)"

# List snapshots
doctl compute snapshot list --resource droplet
```

### SSH Remote Commands

Run commands on the server via SSH:

```bash
ssh root@157.245.133.86 "<command>"
```

Examples:

```bash
# Check server uptime and load
ssh root@157.245.133.86 "uptime"

# Check disk usage
ssh root@157.245.133.86 "df -h /"

# Check memory usage
ssh root@157.245.133.86 "free -h"

# Check running services
ssh root@157.245.133.86 "systemctl list-units --type=service --state=running | grep -E 'ttyd|filebrowser|nginx|login'"

# View login app logs
ssh root@157.245.133.86 "journalctl -u login-app --no-pager -n 50"

# View nginx error log
ssh root@157.245.133.86 "tail -50 /var/log/nginx/error.log"

# View nginx access log
ssh root@157.245.133.86 "tail -50 /var/log/nginx/access.log"
```

### Service Management

The server runs these services:
- **login-app**: FastAPI login page on port 8000
- **nginx**: Reverse proxy on port 80 (and 443 if TLS configured)
- **ttyd-{username}**: Per-user web terminal (ports 9001+)
- **filebrowser-{username}**: Per-user file browser (ports 8001+)

```bash
# Check all biai services
ssh root@157.245.133.86 "systemctl list-units --type=service | grep -E 'ttyd|filebrowser|nginx|login'"

# Restart a specific service
ssh root@157.245.133.86 "systemctl restart login-app"
ssh root@157.245.133.86 "systemctl restart nginx"
ssh root@157.245.133.86 "systemctl restart ttyd-<username>"
ssh root@157.245.133.86 "systemctl restart filebrowser-<username>"

# Check service status
ssh root@157.245.133.86 "systemctl status login-app"

# View port assignments
ssh root@157.245.133.86 "cat /etc/biai-ports"

# Check what's listening on ports
ssh root@157.245.133.86 "ss -tlnp | grep -E ':(80|8000|8001|9001)'"
```

### Deploying Code

The repo is cloned to `/opt/biai-vm/` on the server.

```bash
# Pull latest code on the server
ssh root@157.245.133.86 "cd /opt/biai-vm && git pull"

# Restart services after deploy
ssh root@157.245.133.86 "systemctl restart login-app && systemctl reload nginx"

# Full redeploy: pull + re-provision + restart
ssh root@157.245.133.86 "cd /opt/biai-vm && git pull && bash provision-students.sh"
```

### Student/User Management

```bash
# List current users
ssh root@157.245.133.86 "cat /etc/biai-ports"

# Add a new user manually
ssh root@157.245.133.86 "useradd -m -s /bin/bash -N <username> && echo '<username>:jgsbai' | chpasswd && bash /opt/biai-vm/setup-user.sh <username>"

# Re-provision all students from database
ssh root@157.245.133.86 "cd /opt/biai-vm && source /etc/biai.env && bash provision-students.sh"

# Check a user's workspace
ssh root@157.245.133.86 "ls -la /home/<username>/workspace/"

# Check environment file
ssh root@157.245.133.86 "cat /etc/biai.env"
```

### Nginx Management

```bash
# Regenerate nginx config from /etc/biai-ports
ssh root@157.245.133.86 "bash /opt/biai-vm/generate-nginx.sh"

# View current nginx config
ssh root@157.245.133.86 "cat /etc/nginx/sites-available/biai-vm"

# Test nginx config
ssh root@157.245.133.86 "nginx -t"

# Reload nginx
ssh root@157.245.133.86 "systemctl reload nginx"
```

### TLS/SSL

```bash
# Set up Let's Encrypt certificate
ssh root@157.245.133.86 "certbot --nginx -d vm.kerryback.com"

# Check certificate status
ssh root@157.245.133.86 "certbot certificates"

# Renew certificates
ssh root@157.245.133.86 "certbot renew"
```

### Firewall

```bash
# Check firewall status
ssh root@157.245.133.86 "ufw status verbose"

# Allow HTTP/HTTPS/SSH
ssh root@157.245.133.86 "ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp"
```

### Troubleshooting

```bash
# Check if login app is running
ssh root@157.245.133.86 "systemctl status login-app; ss -tlnp | grep 8000"

# Check all failed services
ssh root@157.245.133.86 "systemctl --failed"

# Check recent system logs
ssh root@157.245.133.86 "journalctl --since '1 hour ago' --no-pager | tail -100"

# Check if a student can reach their terminal
ssh root@157.245.133.86 "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9001/<username>/"

# Check if filebrowser is responding
ssh root@157.245.133.86 "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8001/<username>/files/"
```

## Architecture

```
Internet → nginx (80/443)
            ├── / → login-app.py (8000)
            ├── /login → login-app.py (8000)
            ├── /admin → login-app.py (8000)
            ├── /<user>/ → ttyd (9001+)
            └── /<user>/files/ → filebrowser (8001+)
```

## Notes

- DNS for vm.kerryback.com is managed outside DigitalOcean (not in DO's DNS)
- Default student password: `jgsbai`
- The login app authenticates against Linux PAM (su)
- filebrowser runs with --noauth (auth handled by login app session)
- ttyd runs with --writable to allow terminal input
- Each student's .bashrc auto-launches Claude Code on terminal login
