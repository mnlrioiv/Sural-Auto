import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("PRAGMA table_info(workflow_published_version)")
cols = [r[1] for r in cur.fetchall()]
print("workflow_published_version cols:", cols)
cur.execute(f"SELECT {','.join(cols)} FROM workflow_published_version")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(f"  wfId={d.get('workflowId', '')[:8]} vid={d.get('versionId', '')[:8]}")

print()
cur.execute("SELECT id, name, versionId, activeVersionId FROM workflow_entity")
for r in cur.fetchall():
    print(
        f"wf: {r[0][:8]} | {r[1]} | vid={r[2][:8]} | activeVid={str(r[3])[:8] if r[3] else None}"
    )
db.close()
