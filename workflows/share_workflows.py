import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("PRAGMA table_info(shared_workflow)")
cols = [r[1] for r in cur.fetchall()]
print("shared_workflow cols:", cols)

cur.execute("PRAGMA table_info(project)")
cols = [r[1] for r in cur.fetchall()]
print("project cols:", cols)

# Get project ID
cur.execute("SELECT id FROM project LIMIT 1")
proj = cur.fetchone()
proj_id = proj[0] if proj else None
print(f"Project: {proj_id}")

if proj_id:
    # Get all workflows
    cur.execute("SELECT id FROM workflow_entity")
    for r in cur.fetchall():
        wf_id = r[0]
        cur.execute(
            "SELECT COUNT(*) FROM shared_workflow WHERE workflowId = ?", (wf_id,)
        )
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO shared_workflow (workflowId, projectId) VALUES (?, ?)",
                (wf_id, proj_id),
            )
            print(f"Shared workflow {wf_id[:8]} with project {proj_id[:8]}")
        else:
            print(f"Workflow {wf_id[:8]} already shared")

db.commit()
db.close()
print("\nDone!")
