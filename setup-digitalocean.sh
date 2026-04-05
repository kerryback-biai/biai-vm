#!/bin/bash
# DigitalOcean VM Setup — Coder + Claude Code
# Run as root on a fresh Ubuntu 24.04 droplet
set -e

echo "=== BI-to-AI Workshop VM Setup ==="

# 1. System packages
echo "[1/8] Installing system packages..."
apt-get update -qq
apt-get install -y -qq \
    python3 python3-pip python3-venv \
    git curl wget \
    libreoffice-calc libreoffice-impress libreoffice-writer \
    pandoc poppler-utils \
    nginx certbot python3-certbot-nginx \
    postgresql-client

# 2. Install Node.js 20 (needed for Claude Code and pptxgenjs)
echo "[2/8] Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y -qq nodejs

# 3. Install Claude Code globally
echo "[3/8] Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# 4. npm packages for Office skills
echo "[4/8] Installing npm packages..."
npm install -g pptxgenjs

# 5. Python packages (system-wide)
echo "[5/8] Installing Python packages..."
pip3 install --break-system-packages \
    anthropic duckdb pandas numpy matplotlib \
    fastapi uvicorn httpx \
    openpyxl defusedxml lxml markitdown Pillow \
    psycopg2-binary

# 6. Install code-server
echo "[6/8] Installing code-server..."
curl -fsSL https://code-server.dev/install.sh | sh

# 7. Install Coder
echo "[7/8] Installing Coder..."
curl -fsSL https://coder.com/install.sh | sh

# 8. Create shared directories
echo "[8/8] Setting up shared directories..."
mkdir -p /shared/data /shared/templates /shared/skills

# Copy templates and exercises from repo
if [ -d /opt/biai-vm/templates ]; then
    cp -r /opt/biai-vm/templates/* /shared/templates/
fi
if [ -d /opt/biai-vm/skills ]; then
    cp -r /opt/biai-vm/skills/* /shared/skills/
fi
chmod -R 755 /shared

echo ""
echo "=== System setup complete ==="
echo "Next: run provision-students.sh to create student accounts"
