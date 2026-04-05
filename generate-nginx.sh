#!/bin/bash
# Regenerate nginx config from /etc/biai-ports
set -e

PORTS_FILE="/etc/biai-ports"
NGINX_LOCATIONS=""

BANNER_CSS='<style>#biai-banner{background:#1e1e2e;color:#cdd6f4;text-align:center;padding:6px 0;font-family:system-ui,sans-serif;font-size:13px;letter-spacing:0.3px;position:fixed;top:0;left:0;right:0;z-index:99999;line-height:1.4;border-bottom:1px solid #313244}#biai-banner strong{color:#89b4fa}</style>'
BANNER_HTML='<div id="biai-banner"><strong>AI+Code Lab</strong> &ensp;|&ensp; Rice Business Executive Education &ensp;|&ensp; Professor Kerry Back</div>'

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

        proxy_set_header Accept-Encoding \"\";
        sub_filter '</head>' '${BANNER_CSS}</head>';
        sub_filter '</body>' '${BANNER_HTML}</body>';
        sub_filter_once on;
        sub_filter_types text/html;
    }

    # $USERNAME — file browser
    location /$USERNAME/files/ {
        proxy_pass http://127.0.0.1:$FB_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_http_version 1.1;

        proxy_set_header Accept-Encoding \"\";
        sub_filter '</head>' '${BANNER_CSS}</head>';
        sub_filter '</body>' '${BANNER_HTML}</body>';
        sub_filter_once on;
        sub_filter_types text/html;
    }"
done < "$PORTS_FILE"

cat > /etc/nginx/sites-available/biai-vm << NGINX
server {
    listen 80;
    server_name vm.kerryback.com _;
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
echo "Nginx config regenerated."
