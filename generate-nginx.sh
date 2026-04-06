#!/bin/bash
# Regenerate nginx config from /etc/biai-ports
set -e

PORTS_FILE="/etc/biai-ports"
NGINX_LOCATIONS=""

while IFS=: read -r USERNAME TTYD_PORT FB_PORT; do
    [ -z "$USERNAME" ] && continue
    NGINX_LOCATIONS="$NGINX_LOCATIONS
    # $USERNAME — terminal
    location /$USERNAME/ {
        proxy_pass http://127.0.0.1:$TTYD_PORT;
        proxy_set_header Host \$host;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
    }

    # $USERNAME — file browser
    location /$USERNAME/files/ {
        proxy_pass http://127.0.0.1:$FB_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
    }"
done < "$PORTS_FILE"

cat > /etc/nginx/sites-available/biai-vm << NGINX
server {
    listen 80;
    server_name ai-lab.rice-business.org;
    client_max_body_size 50M;

    # Login page
    location = / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
    location /login {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
    location /workspace {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
$NGINX_LOCATIONS
}
NGINX

ln -sf /etc/nginx/sites-available/biai-vm /etc/nginx/sites-enabled/biai-vm
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# Re-apply SSL certificate if certbot is installed and a cert exists
if command -v certbot &>/dev/null && [ -d /etc/letsencrypt/live/ai-lab.rice-business.org ]; then
    certbot install --cert-name ai-lab.rice-business.org --nginx --redirect --non-interactive 2>/dev/null
    echo "Nginx config regenerated (with SSL)."
else
    echo "Nginx config regenerated (no SSL — run certbot to enable HTTPS)."
fi
