import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT id, name, type, creatorId FROM project")
for r in cur.fetchall():
    print(f"id={r[0]} type={r[2]} creator={r[3]}")

cur.execute("SELECT workflowId, projectId, role FROM shared_workflow")
for r in cur.fetchall():
    print(f"shared_wf: wf={r[0][:8]} proj={r[1][:8]}")

cur.execute("SELECT credentialsId, projectId, role FROM shared_credentials")
for r in cur.fetchall():
    print(f"shared_cred: cred={r[0][:8]} proj={r[1][:8]}")

db.close()
