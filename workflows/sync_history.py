import sqlite3, json
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

cur.execute("SELECT id, name, nodes, connections, versionId FROM workflow_entity")
for r in cur.fetchall():
    wf_id, name, nodes_json, conns_json, vid = r

    cur.execute(
        "UPDATE workflow_history SET nodes = ?, connections = ?, updatedAt = ? WHERE workflowId = ?",
        (nodes_json, conns_json, now, wf_id),
    )
    print(f"Updated workflow_history for {wf_id[:8]} | {name} ({cur.rowcount} rows)")

db.commit()
db.close()
print("\nDone!")
