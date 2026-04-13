import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("PRAGMA table_info(workflow_history)")
cols = [r[1] for r in cur.fetchall()]
print("workflow_history cols:", cols)

cur.execute(f"SELECT {','.join(cols)} FROM workflow_history LIMIT 5")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(
        f"  wfId={d.get('workflowId', '')[:8]} vid={d.get('versionId', '')[:8] if d.get('versionId') else 'N/A'}"
    )

db.close()
