import sqlite3, json, uuid
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

cur.execute("SELECT id, versionId FROM workflow_entity")
for r in cur.fetchall():
    wf_id = r[0]
    vid = r[1]
    cur.execute(
        "INSERT INTO workflow_published_version (workflowId, publishedVersionId, createdAt, updatedAt) VALUES (?, ?, ?, ?)",
        (wf_id, vid, now, now),
    )
    print(f"Published: {wf_id[:8]} with version {vid[:8]}")

db.commit()
db.close()
print("\nDone! Restart n8n to activate workflows.")
