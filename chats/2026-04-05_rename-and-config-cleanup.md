# Chat: Rename repo & config cleanup
**Date:** 2026-04-05
**Repo:** ai-lab (master) — formerly biai-vm

## What was done
- Investigated `.claude` config files: `.claude.json` is missing, 5 backup files and 3 "corrupted" files exist in `~/.claude/backups/` (all valid JSON)
- Renamed GitHub repo from `kerryback-biai/biai-vm` to `kerryback-biai/ai-lab`
- Updated local git remote to new URL
- Fixed SSH config typo: `IHost` → `Host` on line 1 of `~/.ssh/config`
- Found DigitalOcean droplet at 157.245.133.86 (domain: vm.kerryback.com)
- Renamed `/opt/biai-vm` to `/opt/ai-lab` on the droplet
- Updated systemd service (`biai-login.service`) WorkingDirectory and restarted it
- Updated all scripts on the droplet referencing the old path

## Files changed
- `~/.ssh/config` — fixed IHost typo
- Local git remote updated to `kerryback-biai/ai-lab`
- **On droplet:** `/etc/systemd/system/biai-login.service`, plus 5 scripts in `/opt/ai-lab/`

## Next steps
- The `.claude.json` main config file is missing — Claude Code may have regenerated it on startup, but worth monitoring
- The droplet hostname is still `biai-vm` (shown in systemd logs) — cosmetic only, rename via DigitalOcean dashboard if desired
- Local repo directory is still named `biai-vm` — rename locally if desired
