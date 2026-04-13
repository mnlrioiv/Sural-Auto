import sqlite3
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

# Get project ID
cur.execute("SELECT id FROM project LIMIT 1")
proj = cur.fetchone()
proj_id = proj[0]
print(f"Project: {proj_id}")

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# Get all workflows
cur.execute("SELECT id FROM workflow_entity")
for r in cur.fetchall():
    wf_id = r[0]
    cur.execute("SELECT COUNT(*) FROM shared_workflow WHERE workflowId = ?", (wf_id,))
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO shared_workflow (workflowId, projectId, role, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)",
            (wf_id, proj_id, "workflow:owner", now, now),
        )
        print(f"Shared workflow {wf_id[:8]} with role 'workflow:owner'")
    else:
        print(f"Workflow {wf_id[:8]} already shared")

db.commit()
db.close()
print("\nDone!")
