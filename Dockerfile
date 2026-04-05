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

# 2. Install code-server (VS Code in the browser)
RUN curl -fsSL https://code-server.dev/install.sh | sh

# 3. Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# 4. npm packages for Office skills
RUN npm install -g pptxgenjs

# 5. Python packages (system-wide)
RUN pip3 install --break-system-packages \
    anthropic duckdb pandas numpy matplotlib \
    fastapi uvicorn httpx \
    openpyxl defusedxml lxml markitdown Pillow \
    psycopg2-binary

# 6. Create shared directories
RUN mkdir -p /shared/data /shared/templates /shared/skills

# 7. Copy repo contents
COPY templates/ /shared/templates/
COPY exercises/ /shared/exercises/
COPY skills/ /shared/skills/

# 8. Copy entrypoint and database fetch script
COPY fetch-students.py /fetch-students.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
