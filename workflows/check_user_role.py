import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT id, email, role FROM user")
for r in cur.fetchall():
    print(f"user: id={r[0]} email={r[1]} role={r[2]}")
db.close()
