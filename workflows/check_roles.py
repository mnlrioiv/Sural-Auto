import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

# Check role table
cur.execute("PRAGMA table_info(role)")
cols = [r[1] for r in cur.fetchall()]
print("role cols:", cols)
cur.execute("SELECT * FROM role")
for r in cur.fetchall():
    print(f"role: {r}")

# Check scope table
cur.execute("SELECT * FROM scope LIMIT 5")
for r in cur.fetchall():
    print(f"scope: {r}")

# Check role_scope
try:
    cur.execute("PRAGMA table_info(role_scope)")
    cols = [r[1] for r in cur.fetchall()]
    print("role_scope cols:", cols)
    cur.execute("SELECT * FROM role_scope LIMIT 5")
    for r in cur.fetchall():
        print(f"role_scope: {r}")
except:
    print("role_scope not found")

db.close()
