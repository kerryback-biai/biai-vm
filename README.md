# BI-to-AI Linux VM

Linux VM setup and student exercises for the "From BI to AI" executive program. Students SSH in and use Claude Code to build data agents hands-on.

## Exercises

| Exercise | Description | Time |
|:---------|:---------------------------------------------|:---------|
| 1 | Build a 50-line agent that queries one database | ~30 min |
| 2 | Extend it to query two systems and merge results | ~30 min |
| 3 | Wrap it in a web interface | ~45 min |
| 4 | Red-team the agent for security vulnerabilities | ~30 min |

## Setup

```bash
# Provision the VM and install dependencies
bash setup-server.sh

# Create student accounts (preconfigured with course API key)
bash create-students.sh
```
