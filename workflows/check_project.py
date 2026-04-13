import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

print("=== project table ===")
cur.execute("SELECT id, name, type FROM project")
for r in cur.fetchall():
    print(f"  id={r[0]} name={r[1]} type={r[2]}")

print("\n=== shared_workflow ===")
cur.execute("SELECT workflowId, projectId FROM shared_workflow")
for r in cur.fetchall():
    print(f"  wfId={r[0][:8]} projId={r[1][:8] if r[1] else None}")

print("\n=== workflow_entity (with projectId) ===")
cur.execute("PRAGMA table_info(workflow_entity)")
cols = [r[1] for r in cur.fetchall()]
if "projectId" in cols:
    cur.execute("SELECT id, name, projectId FROM workflow_entity")
    for r in cur.fetchall():
        print(
            f"  id={r[0][:8]} name={r[1]} projectId={r[2] if len(cols) > 20 else 'N/A'}"
        )
else:
    print("  No projectId column")

db.close()
