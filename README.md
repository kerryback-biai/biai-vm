# BIAI Lab Server

Linux VM setup and student workspaces for the "Business Intelligence & AI" executive program at Rice Business. Students log in via browser and use Claude Code for hands-on exercises across all eight sessions.

## Session Data

| Directory | Session | Contents |
|:----------|:--------|:---------|
| `data/dashboard/` | Session 2 | Acme Corp CSVs: sales (837 txns), customers (50), employees (30) |
| `data/salesforce/` | Session 4 | Parquet files for building data agents |
| `data/portfolio/` | Session 6 | Wealth management portfolio lots, client profile, stock DB access |

## Skills (pre-installed)

| Skill | Purpose |
|:------|:--------|
| `docx` | Create Word documents via OOXML |
| `xlsx` | Create Excel workbooks with formulas |
| `pptx` | Create PowerPoint presentations |

## Exercise Templates

| Template | Session | Description |
|:---------|:--------|:---------------------------------------------|
| `ex1_hello_agent.py` | 4 | Build a 50-line agent that queries one database |
| `ex2_multi_system.py` | 4 | Extend to query two systems and merge results |
| `ex3_web_app.py` | 4 | Wrap agent in a web interface |
| `ex4_red_team.md` | 5 | Red-team the agent for security vulnerabilities |

## Setup

```bash
# Provision the VM and install dependencies
sudo bash setup-server.sh

# Upload data to /tmp/biai-data/ first, then re-run setup-server.sh
# Or manually: cp -r data/* /shared/data/

# Create student accounts
sudo bash provision-students.sh
```

## Workspace Structure (per student)

```
~/workspace/
├── CLAUDE.md              # Project instructions (business definitions, data locations)
├── data/                  # Symlink to /shared/data
│   ├── dashboard/         # Session 2: Acme Corp CSVs
│   ├── portfolio/         # Session 6: wealth management data
│   └── salesforce/        # Session 4: parquet files for agent exercises
├── ex1_hello_agent.py     # Session 4 exercise templates
├── ex2_multi_system.py
├── ex3_web_app.py
└── ex4_red_team.md
```
