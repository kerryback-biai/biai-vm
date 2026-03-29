#!/bin/bash
# Meridian Corp AI Course — Server Setup
# Run as root on a fresh Ubuntu 24.04 VM
# Usage: sudo bash setup-server.sh

set -e

echo "=== Meridian Corp AI Course Server Setup ==="

# 1. System packages
echo "[1/6] Installing system packages..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nodejs npm git curl

# 2. Install Claude Code globally
echo "[2/6] Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# 3. Python packages (system-wide for all students)
echo "[3/6] Installing Python packages..."
pip3 install --break-system-packages anthropic duckdb pandas numpy matplotlib fastapi uvicorn httpx

# 4. Create shared data directory
echo "[4/6] Setting up shared data..."
mkdir -p /shared/data
# Copy parquet files (assumes they've been uploaded to /tmp/meridian/)
if [ -d /tmp/meridian ]; then
    cp -r /tmp/meridian/* /shared/data/
    echo "  Copied data files from /tmp/meridian/"
else
    echo "  WARNING: /tmp/meridian/ not found. Upload parquet files there first."
fi
chmod -R 755 /shared/data

# 5. Set up shared API key
echo "[5/6] Configuring API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    read -p "Enter Anthropic API key: " API_KEY
else
    API_KEY="$ANTHROPIC_API_KEY"
fi
cat > /etc/profile.d/anthropic.sh << EOF
export ANTHROPIC_API_KEY="$API_KEY"
EOF
chmod 644 /etc/profile.d/anthropic.sh

# 6. Create exercise templates directory
echo "[6/6] Installing exercise templates..."
mkdir -p /shared/templates
cp -r /tmp/templates/* /shared/templates/ 2>/dev/null || echo "  Upload templates to /tmp/templates/ and re-run"
chmod -R 755 /shared/templates

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  1. Upload parquet files to /tmp/meridian/ if not done"
echo "  2. Upload exercise templates to /tmp/templates/ if not done"
echo "  3. Run create-students.sh to create student accounts"
echo ""
