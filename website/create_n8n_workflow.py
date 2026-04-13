#!/usr/bin/env python3
import sqlite3
import json
import time

DB = "/opt/sural/automation/n8n_data/database.sqlite"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT id, name FROM project LIMIT 1")
project = cur.fetchone()
if project:
    project_id = project[0]
    print(f"Using project: {project_id}")
else:
    print("No project found, creating one...")
    project_id = "1"
    cur.execute(
        "INSERT INTO project (id, name, type, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)",
        (
            "1",
            "Default",
            "personal",
            "2026-03-21T00:00:00.000Z",
            "2026-03-21T00:00:00.000Z",
        ),
    )
    conn.commit()
    project_id = "1"

cur.execute("SELECT MAX(id) FROM workflow_entity")
max_id = cur.fetchone()[0] or 0
new_id = max_id + 1

now = "2026-03-21T13:00:00.000Z"

workflow = {
    "name": "Contacto Landing Sural",
    "nodes": [
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
                "options": {},
            },
        },
        {
            "id": "node-slack-1",
            "name": "Notificar a Slack",
            "type": "@n8n/n8n-nodes-base.slack",
            "typeVersion": 3.4,
            "position": [550, 150],
            "parameters": {
                "resource": "message",
                "operation": "send",
                "channel": {"__rl": True, "mode": "name", "value": "#leads"},
                "text": "=Nuevo lead desde landing Sural\n*Nombre:* {{ $json.body.nombre }}\n*Email:* {{ $json.body.email }}\n*Empresa:* {{ $json.body.empresa }}\n*Interés:* {{ $json.body.interes }}",
                "options": {},
            },
        },
        {
            "id": "node-email-1",
            "name": "Email de confirmación",
            "type": "@n8n/n8n-nodes-base.emailSend",
            "typeVersion": 1.6,
            "position": [550, 350],
            "parameters": {
                "to": "={{ $json.body.email }}",
                "subject": "Recibimos tu consulta - Sural",
                "text": "Hola {{ $json.body.nombre }},\n\nGracias por contactarnos. Te responderemos en las próximas 24 horas.\n\nEl equipo de Sural",
                "options": {},
            },
        },
        {
            "id": "node-respond-1",
            "name": "Responder",
            "type": "@n8n/n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.4,
            "position": [850, 300],
            "parameters": {
                "respondWith": {
                    "__rl": True,
                    "mode": "json",
                    "value": '={\n  "status": "ok",\n  "message": "¡Consulta recibida! Te contactaremos pronto."\n}',
                },
                "options": {},
            },
        },
    ],
    "connections": {
        "Webhook Contacto": {
            "main": [
                [
                    {"node": "Notificar a Slack", "type": "main", "index": 0},
                    {"node": "Email de confirmación", "type": "main", "index": 0},
                ]
            ]
        },
        "Notificar a Slack": {
            "main": [[{"node": "Responder", "type": "main", "index": 0}]]
        },
        "Email de confirmación": {
            "main": [[{"node": "Responder", "type": "main", "index": 0}]]
        },
    },
    "settings": {"executionOrder": "v1"},
    "staticData": None,
    "pinData": None,
    "versionId": str(new_id),
    "triggerCount": 1,
    "meta": {"templateId": "", "templateName": ""},
    "description": "Recibe leads del formulario de contacto y los procesa automaticamente",
    "isArchived": False,
    "versionCounter": 1,
    "active": 0,
}

cur.execute(
    """
    INSERT INTO workflow_entity 
    (id, name, active, nodes, connections, settings, staticData, pinData, versionId, triggerCount, meta, description, isArchived, versionCounter, createdAt, updatedAt)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        new_id,
        workflow["name"],
        workflow["active"],
        json.dumps(workflow["nodes"]),
        json.dumps(workflow["connections"]),
        json.dumps(workflow["settings"]),
        workflow["staticData"],
        workflow["pinData"],
        workflow["versionId"],
        workflow["triggerCount"],
        json.dumps(workflow["meta"]),
        workflow["description"],
        workflow["isArchived"],
        workflow["versionCounter"],
        now,
        now,
    ),
)

cur.execute(
    """
    INSERT INTO shared_workflow (workflowId, projectId, role, createdAt, updatedAt)
    VALUES (?, ?, ?, ?, ?)
""",
    (new_id, project_id, "workflow:editor", now, now),
)

conn.commit()
print(f"Workflow inserted: id={new_id}, name='{workflow['name']}'")
conn.close()
