import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("PRAGMA table_info(user)")
cols = [r[1] for r in cur.fetchall()]
print("user cols:", cols)
cur.execute("SELECT * FROM user")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(f"user: id={d['id'][:20]} email={d['email']}")
db.close()
