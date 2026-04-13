import sqlite3, json
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

cur.execute("SELECT id, name, nodes, connections, versionId FROM workflow_entity")
for r in cur.fetchall():
    wf_id, name, nodes_json, conns_json, vid = r

    # Check if already in workflow_history
    cur.execute("SELECT COUNT(*) FROM workflow_history WHERE workflowId = ?", (wf_id,))
    if cur.fetchone()[0] > 0:
        print(f"Already exists: {wf_id[:8]} | {name}")
        continue

    # Get nodes and connections
    nodes = json.loads(nodes_json)
    conns = json.loads(conns_json)

    cur.execute(
        """
        INSERT INTO workflow_history 
        (versionId, workflowId, authors, createdAt, updatedAt, nodes, connections, name, autosaved, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (vid, wf_id, "[]", now, now, nodes_json, conns_json, name, 0, ""),
    )
    print(f"Added to workflow_history: {wf_id[:8]} | {name} | vid={vid[:8]}")

db.commit()
db.close()
print("\nDone!")
