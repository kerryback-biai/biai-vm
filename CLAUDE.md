# BIAI Lab Server

Multi-user AI/data agent development platform for Rice Business Executive Education. Provides isolated workspaces with Claude Code (via ttyd terminal) and FileBrowser per student on a shared DigitalOcean Ubuntu 24.04 VM.

- **Domain:** `ai-lab.rice-business.org`
- **Hostname:** `ai-lab`
- **Droplet:** `biai-vm` (DigitalOcean, nyc1, 4GB/2vCPU)
- **IP:** `157.245.133.86`

## Architecture

```
Browser → nginx (80 → 301 redirect, 443 SSL via certbot)
  ├── /            → login-app.py (FastAPI on port 8000)
  ├── /login       → login-app.py
  ├── /workspace   → login-app.py (split-pane workspace: files + terminal)
  ├── /admin       → login-app.py admin panel (DB is_admin check)
  ├── /<user>/     → ttyd terminal (port 9001+)
  └── /<user>/files/ → FileBrowser (port 10001+)
```

After login, users see a single-page workspace with:

- **Left pane (30%):** FileBrowser (file tree)
- **Right pane (70%):** ttyd terminal (Claude Code)
- **Draggable divider** between panes
- **Rice Blue toolbar** at top with username, admin link (if admin), and logout

## User Setup

Each user gets:

- Linux account (no sudo) + home directory
- `ttyd` systemd service (`ttyd-<user>`) — terminal with Claude Code
- `filebrowser` systemd service (`filebrowser-<user>`) — file browser with `--noauth` and `perm.admin=false`
- Workspace at `/home/<user>/workspace/` with exercise templates and symlinked shared data (`/shared/data`)
- Claude Code settings at `/home/<user>/.claude/settings.json` (pre-approved tool permissions)
- Claude Code skills copied from `/shared/skills/`
- `ANTHROPIC_API_KEY` exported in `.bashrc`
- `.bashrc` auto-launches `claude` on terminal open

### Port Registry

`/etc/biai-ports` maps users to ports: `username:ttyd_port:filebrowser_port`

ttyd ports start at 9001, FileBrowser ports start at 10001.

## Admin Access (Two Levels)

### 1. Login app admin panel (`/admin`)

- Controlled by `is_admin` field in the Koyeb PostgreSQL database (NOT Linux sudo group)
- Admins see an "Admin" link in the workspace toolbar
- Allows adding/deleting users on the VM
- Both `kerry_back` and `kelcie_wold` have `is_admin=true`

### 2. FileBrowser admin (Settings/Admin menus)

- Controlled by `perm.admin` in each user's FileBrowser database (`~/.filebrowser.db`)
- Only `kerry_back` has FileBrowser admin enabled
- All other users (including `kelcie_wold`) have `perm.admin=false`

### 3. Server sudo

- Only the `admin` Linux user has sudo privileges
- `kerry_back` and `kelcie_wold` do NOT have sudo

## User Provisioning (Two Paths)

### 1. Database-driven

- Koyeb PostgreSQL (`biai-db`) stores users with `vm_password` field
- `fetch-students.py` queries active users with a `vm_password`; `provision-students.sh` creates Linux accounts + services
- Run manually: `sudo bash provision-students.sh`
- User management (add/edit/delete, passwords, spending limits) is done via the separate `biai-admin` web app deployed on Koyeb

### 2. Admin panel (runtime)

- Admins log in at `ai-lab.rice-business.org` and add/delete users at `/admin`
- Default password for new users: `jgsb!ai!`
- Calls `setup-user.sh` which creates the Linux user, workspace, services, registers in `/etc/biai-ports`, and regenerates nginx

## Key Files

| File                      | Purpose                                                                                                                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `login-app.py`          | FastAPI login + workspace + admin panel (port 8000). Auth via Linux PAM (`su`). Admin check via Koyeb DB `is_admin`. Sessions in memory, 12h expiry. Runs as `biai-login.service`. |
| `setup-server.sh`       | One-time system setup on fresh Ubuntu 24.04 (packages, Claude Code, Python deps, shared dirs)                                                                                            |
| `setup-user.sh`         | Provision a single user: create account, workspace, ttyd + filebrowser services (with `perm.admin=false`), update nginx                                                                |
| `provision-students.sh` | Bulk-provision users from PostgreSQL database via `fetch-students.py`                                                                                                                  |
| `fetch-students.py`     | Queries `users` table for active users with `vm_password` set                                                                                                                        |
| `generate-nginx.sh`     | Reads `/etc/biai-ports` and regenerates nginx config with per-user location blocks. Preserves SSL by re-running `certbot install` after regeneration.                                |
| `nginx-biai-vm.conf`    | Template/reference nginx config                                                                                                                                                          |
| `setup-digitalocean.sh` | DigitalOcean droplet-specific setup (nginx, certbot, Coder)                                                                                                                              |
| `create-students.sh`    | Legacy CSV import (reads `username,password` pairs)                                                                                                                                    |
| `Dockerfile`            | Legacy container build (not currently used — VM deployment is primary)                                                                                                                  |
| `entrypoint.sh`         | Legacy Docker entrypoint                                                                                                                                                                 |

## Environment Variables

| Variable              | Purpose                                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_API_KEY` | Claude API key, exported to all user shells                                                              |
| `DATABASE_URL`      | Koyeb PostgreSQL connection string (used by `fetch-students.py` and `login-app.py` for admin checks) |

Stored in `/etc/biai.env` (sourced by systemd services and scripts) and `/etc/profile.d/anthropic.sh` (system-wide shell export).

## Common Operations

```bash
# Add a user manually
sudo bash setup-user.sh <username>

# Bulk provision from database
sudo bash provision-students.sh

# Regenerate nginx after port changes (preserves SSL)
sudo bash generate-nginx.sh

# Check user services
systemctl status ttyd-<username> filebrowser-<username>

# Restart login app
systemctl restart biai-login

# Check login app logs
journalctl -u biai-login -f
```

## Deployment

- **VM (DigitalOcean):** Run `setup-server.sh` then `provision-students.sh` on Ubuntu 24.04
- SSL via certbot (auto-renewed), domain `ai-lab.rice-business.org`

## Style

Login page and workspace toolbar use Rice brand colors: Rice Blue `#00205B`, Rice Gray `#7C7E7F`, white card backgrounds.
