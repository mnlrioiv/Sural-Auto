import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("PRAGMA table_info(webhook_entity)")
cols = [r[1] for r in cur.fetchall()]
print("webhook_entity columns:", cols)
cur.execute("SELECT * FROM webhook_entity")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(
        f"  wfId={d.get('workflowId', '')[:8]} path={d.get('path', '')} method={d.get('method', '')}"
    )

print("\nworkflow_entity:")
cur.execute("SELECT id, name, active, triggerCount FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r[0]} | {r[1]} | active={r[2]} triggers={r[3]}")
db.close()
