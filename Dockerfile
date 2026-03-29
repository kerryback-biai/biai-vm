FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. System packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    nodejs npm \
    git curl wget \
    libreoffice-calc libreoffice-impress libreoffice-writer \
    pandoc poppler-utils \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# 2. Install ttyd (web-based terminal)
RUN wget -qO /usr/local/bin/ttyd \
    https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 \
    && chmod +x /usr/local/bin/ttyd

# 3. Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# 4. npm packages for Office skills
RUN npm install -g pptxgenjs

# 5. Python packages (system-wide)
RUN pip3 install --break-system-packages \
    anthropic duckdb pandas numpy matplotlib \
    fastapi uvicorn httpx \
    openpyxl defusedxml lxml markitdown Pillow

# 6. Create shared directories
RUN mkdir -p /shared/data /shared/templates /shared/skills

# 7. Copy repo contents
COPY templates/ /shared/templates/
COPY exercises/ /shared/exercises/
COPY skills/ /shared/skills/

# 8. Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
