"""Fetch VM students from shared Postgres database.

Prints username:password pairs (one per line) for active users with ai-lab
service access. The vm_password column stores the plaintext password needed
by Linux chpasswd (the main password_hash column uses bcrypt).
"""
import os
import sys
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    sys.exit(0)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("""
    SELECT username, vm_password
    FROM users
    WHERE is_active = TRUE
      AND vm_password IS NOT NULL
""")
for username, password in cur.fetchall():
    print(f"{username}:{password}")
cur.close()
conn.close()
