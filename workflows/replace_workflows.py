import sqlite3, json, uuid
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

workflows_file = "/tmp/n8n_workflows_v3.json"
with open(workflows_file) as f:
    workflows = json.load(f)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

to_delete = ["zYOskqzKJNvMmayO", "MZydQWJjP9Fe5ZoS"]
for wid in to_delete:
    cur.execute("DELETE FROM webhook_entity WHERE workflowId = ?", (wid,))
    cur.execute("DELETE FROM shared_workflow WHERE workflowId = ?", (wid,))
    cur.execute("DELETE FROM workflows_tags WHERE workflowId = ?", (wid,))
    cur.execute("DELETE FROM workflow_entity WHERE id = ?", (wid,))
    print(f"Deleted {wid[:8]}")

for wf in workflows:
    wf_id = str(uuid.uuid4())
    nodes_json = json.dumps(wf["nodes"])
    conn_json = json.dumps(wf["connections"])

    cur.execute(
        """
        INSERT INTO workflow_entity 
        (id, name, nodes, connections, settings, staticData, pinData, 
         versionId, triggerCount, meta, parentFolderId, createdAt, updatedAt, 
         isArchived, versionCounter, description, active, activeVersionId) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            wf_id,
            wf["name"],
            nodes_json,
            conn_json,
            json.dumps({}),
            None,
            "{}",
            str(uuid.uuid4()),
            0,
            None,
            None,
            now,
            now,
            0,
            1,
            "",
            1,
            None,
        ),
    )
    print(f"Inserted: {wf['name']} (id={wf_id[:8]})")

db.commit()
db.close()
print("\nDone!")
