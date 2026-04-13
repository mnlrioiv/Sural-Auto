import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute(
    "SELECT id, workflowId, versionId, versionId FROM workflow_published_version"
)
for r in cur.fetchall():
    print(f"id={r[0]} wfId={r[1][:8]} versionId={r[2]}")

cur.execute("SELECT id, name, versionId, activeVersionId FROM workflow_entity")
for r in cur.fetchall():
    print(
        f"wf: {r[0][:8]} | {r[1]} | vid={r[2][:8]} | activeVid={str(r[3])[:8] if r[3] else None}"
    )

db.close()
