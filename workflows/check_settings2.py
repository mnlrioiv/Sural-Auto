import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT name, value FROM settings WHERE name LIKE '%owner%' OR name LIKE '%setup%'"
)
for r in cur.fetchall():
    print(f"{r[0]} = {r[1]}")
db.close()
