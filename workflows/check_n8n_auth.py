import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("SELECT id, email, role, isOwner, isInstanceOwner FROM user")
for r in cur.fetchall():
    print(f"id={r[0]} email={r[1]} role={r[2]} isOwner={r[3]} isInstanceOwner={r[4]}")

cur.execute(
    "SELECT name, value FROM settings WHERE name IN ('userId', 'isInstanceOwnerSetUp', 'n8n_api_key')"
)
for r in cur.fetchall():
    print(f"  setting: {r[0]} = {str(r[1])[:50]}")

db.close()
