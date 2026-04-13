import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT id, workflowId, status, error, finished, startedAt FROM execution_entity ORDER BY startedAt DESC LIMIT 15"
)
print("Recent executions:")
for r in cur.fetchall():
    err = str(r[3])[:200] if r[3] else None
    print(f"id={r[0][:8]} wfId={r[1][:8]} status={r[2]} finished={r[4]} error={err}")

print("\nAll workflows:")
cur.execute(
    "SELECT id, name, active, triggerCount, lastExecutedAt FROM workflow_entity"
)
for r in cur.fetchall():
    print(f"  {r[0]} | {r[1]} | active={r[2]} triggers={r[3]} lastExec={r[4]}")
db.close()
