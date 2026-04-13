import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%credential%'"
)
for r in cur.fetchall():
    print(r[0])
db.close()
