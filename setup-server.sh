#!/bin/bash
# Meridian Corp AI Course — Server Setup
# Run as root on a fresh Ubuntu 24.04 VM
# Usage: sudo bash setup-server.sh

set -e

echo "=== Meridian Corp AI Course Server Setup ==="

# 1. System packages
echo "[1/7] Installing system packages..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nodejs npm git curl \
    libreoffice-calc libreoffice-impress libreoffice-writer \
    pandoc poppler-utils

# 2. Install Claude Code globally
echo "[2/7] Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# 3. npm packages for Office skills (pptxgenjs for slide creation)
echo "[3/7] Installing npm packages..."
npm install -g pptxgenjs

# 4. Python packages (system-wide for all students)
echo "[4/7] Installing Python packages..."
pip3 install --break-system-packages anthropic duckdb pandas numpy matplotlib fastapi uvicorn httpx \
    openpyxl defusedxml lxml markitdown Pillow

# 5. Create shared data directory
echo "[5/7] Setting up shared data..."
mkdir -p /shared/data
# Copy parquet files (assumes they've been uploaded to /tmp/meridian/)
if [ -d /tmp/meridian ]; then
    cp -r /tmp/meridian/* /shared/data/
    echo "  Copied data files from /tmp/meridian/"
else
    echo "  WARNING: /tmp/meridian/ not found. Upload parquet files there first."
fi
chmod -R 755 /shared/data

# 6. Set up shared API key
echo "[6/7] Configuring API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    read -p "Enter Anthropic API key: " API_KEY
else
    API_KEY="$ANTHROPIC_API_KEY"
fi
cat > /etc/profile.d/anthropic.sh << EOF
export ANTHROPIC_API_KEY="$API_KEY"
EOF
chmod 644 /etc/profile.d/anthropic.sh

# 7. Create exercise templates and skills directories
echo "[7/7] Installing exercise templates and Claude Code skills..."
mkdir -p /shared/templates
cp -r /tmp/templates/* /shared/templates/ 2>/dev/null || echo "  Upload templates to /tmp/templates/ and re-run"
chmod -R 755 /shared/templates

# Claude Code skills (xlsx, docx, pptx) — shared source for all students
mkdir -p /shared/skills
if [ -d /tmp/skills ]; then
    cp -r /tmp/skills/* /shared/skills/
    echo "  Copied skills from /tmp/skills/"
else
    echo "  WARNING: /tmp/skills/ not found. Upload skill directories there first."
    echo "  Expected structure: /tmp/skills/xlsx/SKILL.md, /tmp/skills/docx/SKILL.md, /tmp/skills/pptx/SKILL.md"
fi
chmod -R 755 /shared/skills

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  1. Upload parquet files to /tmp/meridian/ if not done"
echo "  2. Upload exercise templates to /tmp/templates/ if not done"
echo "  3. Upload Claude Code skills to /tmp/skills/ if not done"
echo "     (xlsx/, docx/, pptx/ directories each containing SKILL.md)"
echo "  4. Run create-students.sh to create student accounts"
echo ""
