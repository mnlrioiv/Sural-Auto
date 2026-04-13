import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
print("=== webhook_entity ===")
cur.execute(
    "SELECT id, workflowId, path, method, node, webhookPath, pathA, pathB FROM webhook_entity"
)
for r in cur.fetchall():
    print(f"  id={r[0]} wfId={r[1][:8]} path={r[2]} method={r[3]} node={r[4]}")

print("\n=== workflow_entity ===")
cur.execute("SELECT id, name, active, triggerCount FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r[0]} | {r[1]} | active={r[2]} triggers={r[3]}")

print("\n=== webhook_entity count ===")
cur.execute("SELECT COUNT(*) FROM webhook_entity")
print(f"  {cur.fetchone()[0]} webhooks")

db.close()
