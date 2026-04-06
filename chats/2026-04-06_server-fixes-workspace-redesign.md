# Chat: Server fixes, workspace redesign, auto-provisioning
**Date:** 2026-04-06
**Repo:** biai-lab (master) + biai-admin (master)

## What was done
- **Fixed HTTPS outage**: `generate-nginx.sh` had overwritten certbot SSL config; restored SSL and made script preserve it
- **Updated server_name** from `vm.kerryback.com` to `ai-lab.rice-business.org`; changed hostname to `ai-lab`
- **Built split-pane workspace**: Single page with file tree (left, 40%) + terminal (right, 60%) with draggable divider and Rice Blue toolbar — replaces old two-tab launch
- **Renamed AI+Code Lab to AI Lab** everywhere
- **Switched admin check** from Linux sudo group to Koyeb PostgreSQL `is_admin` field
- **Eliminated FileBrowser login**: Configured proxy auth (`X-FB-User` header) with nginx-injected auto-login JS
- **Disabled FileBrowser admin menus** for all users except `kerry_back`
- **Removed legacy admin link** from workspace toolbar (user mgmt via biai-admin Koyeb app)
- **Created `biai-login.service`** systemd unit with `DATABASE_URL` + `PROVISION_SECRET`
- **Built auto-provisioning**: Added `POST /provision` endpoint to login-app.py (secret-secured); biai-admin now calls it on user create, bulk create, and password reset
- **Synced passwords** for existing users to match DB values

## Files changed (biai-lab)
- `login-app.py` — workspace page, DB admin, `/provision` endpoint
- `generate-nginx.sh` — SSL preservation, proxy auth for FileBrowser, `/provision` route
- `setup-user.sh` — FileBrowser proxy auth, perm.admin=false for new users
- `nginx-biai-vm.conf` — updated server_name
- `CLAUDE.md` — full rewrite

## Files changed (biai-admin)
- `app/admin/routes.py` — calls VM `/provision` on user create/bulk/password reset
- `app/config.py` — added `vm_provision_url` and `provision_secret` settings
- `requirements.txt` — added `httpx`

## Next steps
- `provision-students.sh` still has outdated nginx generation and old naming — should delegate to `generate-nginx.sh`
- Legacy files (`Dockerfile`, `entrypoint.sh`, `create-students.sh`) could be cleaned up
- Unused admin routes in `login-app.py` could be removed
- Verify Koyeb deploy completed and test end-to-end: add user in admin → auto-login on VM
