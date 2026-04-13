import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT id, name, type FROM credentials_entity")
for r in cur.fetchall():
    print(f"id={r[0]} name={r[1]} type={r[2]}")

cur.execute("SELECT credentialsId, projectId, role FROM shared_credentials")
for r in cur.fetchall():
    print(f"shared: credId={r[0]} projId={r[1]} role={r[2]}")

cur.execute("SELECT id, name, type FROM installed_nodes")
for r in cur.fetchall():
    if "email" in str(r).lower():
        print(f"node: {r}")
db.close()
