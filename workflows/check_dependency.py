import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT * FROM workflow_dependency")
for r in cur.fetchall():
    print(r)
db.close()
