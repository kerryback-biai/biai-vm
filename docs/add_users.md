# Adding Users

Users are managed through the Meridian admin API. Both the Meridian web app and the Claude Code VM share the same user database.

## Prerequisites

Get an admin token (valid for 24 hours):

```bash
TOKEN=$(curl -s https://meridian.kerryback.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"YOUR_ADMIN_PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
```

## Add a single user

```bash
curl -s https://meridian.kerryback.com/api/admin/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jsmith",
    "password": "TempPass123",
    "name": "Jane Smith",
    "apps": ["meridian", "vm"]
  }'
```

The `apps` field controls which services the user can access:

| Value | Access |
|-------|--------|
| `["meridian"]` | Meridian web app only (default) |
| `["vm"]` | Claude Code VM only |
| `["meridian", "vm"]` | Both |

## Bulk upload from CSV

Create a CSV file (e.g., `students.csv`):

```csv
username,password,name,spending_limit,apps
jsmith,TempPass123,Jane Smith,10,meridian,vm
mjones,TempPass456,Mike Jones,10,meridian,vm
alee,TempPass789,Amy Lee,10,meridian,vm
```

Columns:
- **username** (required) — login name
- **password** (required) — initial password
- **name** (optional) — display name
- **spending_limit** (optional) — API spending cap in dollars (default: $10)
- **apps** (optional) — comma-separated list of apps (default: `meridian`)

Upload:

```bash
curl -s https://meridian.kerryback.com/api/admin/users/bulk \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@students.csv"
```

The response lists which users were created and which were skipped (already exist):

```json
{"created": ["jsmith", "mjones", "alee"], "skipped": []}
```

## After adding users

The VM creates Linux accounts at startup. To pick up newly added users, redeploy the VM:

```bash
export KOYEB_TOKEN=YOUR_KOYEB_TOKEN
koyeb services redeploy biai-vm --app biai-vm
```

Meridian web app access is immediate — no redeploy needed.

## List existing users

```bash
curl -s https://meridian.kerryback.com/api/admin/users \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## Update a user

```bash
curl -s -X PATCH https://meridian.kerryback.com/api/admin/users/USER_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

Updatable fields: `name`, `is_active`, `is_admin`, `spending_limit_cents`.
