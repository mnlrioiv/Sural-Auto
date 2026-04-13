import sqlite3, json, uuid

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

test_wf = {
    "name": "Test Minimal",
    "nodes": [
        {
            "parameters": {
                "httpMethod": {"__rl": True, "mode": "list", "value": "POST"},
                "path": "test-minimal",
                "responseMode": "lastNode",
                "options": {},
            },
            "id": "wh-test",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "webhookId": "test-minimal",
            "position": [250, 300],
        },
        {
            "parameters": {"jsCode": "return [{json: {message: 'hello'}}];"},
            "id": "code-test",
            "name": "Code",
            "type": "n8n-nodes-base.code",
            "typeVersion": 1,
            "position": [550, 300],
        },
        {
            "parameters": {
                "respondWith": {"__rl": True, "mode": "json", "value": '{"ok": true}'},
                "options": {},
            },
            "id": "resp-test",
            "name": "Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1,
            "position": [850, 300],
        },
    ],
    "connections": {
        "Webhook": {"main": [[{"node": "Code", "type": "main", "index": 0}]]},
        "Code": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]},
    },
    "active": False,
    "settings": {},
    "staticData": None,
    "tags": [],
    "meta": None,
    "pinData": {},
}

wf_id = str(uuid.uuid4())
now = "2026-03-21T15:00:00.000Z"
proj_id = "Bmv03objZqb84raI"

cur.execute(
    """
    INSERT INTO workflow_entity 
    (id, name, nodes, connections, active, createdAt, updatedAt, triggerCount, lastExecutedAt, settings, staticData, tags, meta, pinData, publishedVersion, projectId) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        wf_id,
        test_wf["name"],
        json.dumps(test_wf["nodes"]),
        json.dumps(test_wf["connections"]),
        0,
        now,
        now,
        0,
        None,
        json.dumps({}),
        None,
        "[]",
        None,
        "{}",
        0,
        proj_id,
    ),
)
db.commit()
print(f"Created test workflow: {wf_id}")

# Now activate via CLI
print(f"\nNow activating via n8n CLI...")
db.close()
