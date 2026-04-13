import sqlite3, json, uuid
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

workflows_file = "/tmp/n8n_workflows_v3.json"
with open(workflows_file) as f:
    workflows = json.load(f)

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

# Delete ALL existing workflows and webhooks
cur.execute("DELETE FROM webhook_entity")
cur.execute("DELETE FROM shared_workflow")
cur.execute("DELETE FROM workflows_tags")
cur.execute("DELETE FROM workflow_entity")
print("Deleted all existing workflows")

for wf in workflows:
    wf_id = str(uuid.uuid4())
    nodes_json = json.dumps(wf["nodes"])
    conn_json = json.dumps(wf["connections"])
    vid = str(uuid.uuid4())

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
            vid,
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

    # Register webhooks
    for node in wf["nodes"]:
        if node.get("type") == "n8n-nodes-base.webhook":
            path = node.get("parameters", {}).get("path", "")
            method = (
                node.get("parameters", {}).get("httpMethod", {}).get("value", "POST")
            )
            if path:
                cur.execute(
                    "INSERT INTO webhook_entity (workflowId, webhookPath, method, node) VALUES (?, ?, ?, ?)",
                    (wf_id, path, method, node["name"]),
                )
                print(f"  Webhook registered: {path}")

    print(f"Inserted: {wf['name']} (id={wf_id})")

db.commit()
db.close()
print("\nDone!")
