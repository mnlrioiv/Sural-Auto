import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT * FROM shared_credentials")
for r in cur.fetchall():
    print(r)

cur.execute("SELECT id, name, type FROM credentials_entity")
for r in cur.fetchall():
    print(f"cred: {r}")

cur.execute("SELECT * FROM project_relation")
for r in cur.fetchall():
    print(f"proj_rel: {r}")
db.close()
