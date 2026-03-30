"""Fetch VM students from shared Postgres database.

Prints username:password pairs (one per line) for users with vm app access.
Passwords are stored as bcrypt hashes in the database, so we store plaintext
passwords in a separate column on app_access for VM use (Linux chpasswd needs them).
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
    SELECT u.username, a.vm_password
    FROM users u
    JOIN app_access a ON u.id = a.user_id
    WHERE a.app_name = 'vm'
      AND u.is_active = TRUE
      AND a.vm_password IS NOT NULL
""")
for email, password in cur.fetchall():
    print(f"{email}:{password}")
cur.close()
conn.close()
