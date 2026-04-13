import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

# Check if instance owner is set up
cur.execute("SELECT value FROM settings WHERE name = 'isInstanceOwnerSetUp'")
row = cur.fetchone()
print(f"isInstanceOwnerSetUp: {row[0] if row else 'NOT FOUND'}")

# Deactivate broken workflows
broken = ["zYOskqzKJNvMmayO", "MZydQWJjP9Fe5ZoS"]
for wid in broken:
    cur.execute("UPDATE workflow_entity SET active = 0 WHERE id = ?", (wid,))
    print(f"Deactivated {wid}")

# Delete broken webhooks
for wid in broken:
    cur.execute("DELETE FROM webhook_entity WHERE workflowId = ?", (wid,))
    print(f"Deleted webhooks for {wid}")

db.commit()

# List remaining workflows
cur.execute("SELECT id, name, active FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r[0]} | {r[1]} | active={r[2]}")
db.close()
