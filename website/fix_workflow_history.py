#!/usr/bin/env python3
import sqlite3
import json

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

now = "2026-03-21T13:00:00.000Z"

cur.execute("SELECT * FROM workflow_history LIMIT 1")
cols = [desc[0] for desc in cur.description] if cur.description else []
print("workflow_history columns:", cols)

cur.execute("DELETE FROM workflow_history WHERE workflowId = 1")

cur.execute(
    """
    INSERT INTO workflow_history (versionId, workflowId, authors, createdAt, updatedAt, nodes, connections, name, autosaved)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        "1",
        1,
        "[]",
        now,
        now,
        json.dumps(
            [
                {
                    "id": "node-webhook-1",
                    "name": "Webhook Contacto",
                    "type": "@n8n/n8n-nodes-base.webhook",
                    "typeVersion": 2.2,
                    "position": [250, 300],
                    "webhookId": "contacto-sural",
                    "parameters": {
                        "httpMethod": {"__rl": True, "mode": "list", "value": "POST"},
                        "path": "contacto-sural",
                        "responseMode": "lastNode",
                    },
                }
            ]
        ),
        json.dumps(
            {
                "Webhook Contacto": {
                    "main": [
                        [
                            {"node": "Notificar a Slack", "type": "main", "index": 0},
                            {
                                "node": "Email de confirmación",
                                "type": "main",
                                "index": 0,
                            },
                        ]
                    ]
                }
            }
        ),
        "Contacto Landing Sural",
        0,
    ),
)

conn.commit()
print(
    "workflow_history entries:",
    cur.execute("SELECT * FROM workflow_history WHERE workflowId = 1").fetchall(),
)
conn.close()
