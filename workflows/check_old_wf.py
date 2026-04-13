import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

# Check the old working workflows
cur.execute(
    "SELECT id, name, versionId, activeVersionId FROM workflow_entity WHERE name IN ('Marketing Nurturing Sequence', 'Weekly Follow-up')"
)
for r in cur.fetchall():
    print(
        f"OLD wf: {r[0]} | {r[1]} | vid={r[2][:8]} | avid={r[3][:8] if r[3] else 'NULL'}"
    )

# Check shared_workflow for old workflows
old_ids = ["NbZql7puc6e3Kygt", "xJ9DEY4rYscYU5vw"]
for wid in old_ids:
    cur.execute(
        "SELECT workflowId, projectId FROM shared_workflow WHERE workflowId = ?", (wid,)
    )
    rows = cur.fetchall()
    print(f"shared_workflow for {wid[:8]}: {rows}")

# Check for the project relation
cur.execute("SELECT workflowId, projectId FROM shared_workflow")
for r in cur.fetchall():
    print(f"shared_workflow: wf={r[0][:8]} proj={r[1][:8]}")

# Check project table
cur.execute("SELECT id, name, type FROM project")
for r in cur.fetchall():
    print(f"project: id={r[0]} name={r[1]} type={r[2]}")

# Check isArchived
cur.execute("SELECT id, name, isArchived FROM workflow_entity")
for r in cur.fetchall():
    print(f"wf {r[0][:8]} | {r[1]} | archived={r[2]}")

db.close()
