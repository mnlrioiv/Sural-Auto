#!/usr/bin/env python3
import sqlite3
import json
import os

N8N_DB = "/opt/sural/automation/n8n_data/sqlite.db"

workflow = {
    "name": "Contacto Landing Sural",
    "nodes": [
        {
            "id": "webhook-contacto",
            "name": "Webhook Contacto",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [250, 300],
            "parameters": {
                "httpMethod": "POST",
                "path": "contacto-sural",
                "responseMode": "lastNode",
                "options": {},
            },
            "webhookId": "contacto-sural",
        },
        {
            "id": "slack-notify",
            "name": "Notificar a Slack",
            "type": "n8n-nodes-base.slack",
            "typeVersion": 3,
            "position": [550, 200],
            "parameters": {
                "resource": "message",
                "operation": "send",
                "channel": {"mode": "name", "value": "#leads-sural"},
                "text": "=Nuevo lead desde landing page:\n*Nombre:* {{ $json.nombre }}\n*Empresa:* {{ $json.empresa }}\n*Email:* {{ $json.email }}\n*Teléfono:* {{ $json.telefono }}\n*Interés:* {{ $json.interes }}\n*Mensaje:* {{ $json.mensaje }}",
                "options": {},
            },
            "credentials": {"slackApi": {"__rl": True, "mode": "server", "value": ""}},
        },
        {
            "id": "twilio-ws",
            "name": "WhatsApp Lead",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [550, 400],
            "parameters": {
                "url": "https://api.chatwoot.io/v1/conversations",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "Content-Type", "value": "application/json"}
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "inbox_id", "value": "1"},
                        {"name": "contact", "value": "={{ $json.email }}"},
                    ]
                },
                "options": {},
            },
        },
        {
            "id": "google-sheets",
            "name": "Guardar en Google Sheets",
            "type": "n8n-nodes-base.googleSheets",
            "typeVersion": 4.4,
            "position": [550, 600],
            "parameters": {
                "operation": "append",
                "sheet": {"__rl": True, "mode": "list", "value": ""},
                "options": {"valueInputMode": "USER_ENTERED"},
            },
        },
        {
            "id": "respond-200",
            "name": "Responder 200",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1,
            "position": [850, 300],
            "parameters": {
                "respondWith": {
                    "respondWith": "json",
                    "responseBody": '={"status":"ok","message":"Consulta recibida. Te contactaremos pronto."}',
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
                    {"node": "WhatsApp Lead", "type": "main", "index": 0},
                    {"node": "Guardar en Google Sheets", "type": "main", "index": 0},
                ]
            ]
        },
        "Notificar a Slack": {
            "main": [[{"node": "Responder 200", "type": "main", "index": 0}]]
        },
        "WhatsApp Lead": {
            "main": [[{"node": "Responder 200", "type": "main", "index": 0}]]
        },
        "Guardar en Google Sheets": {
            "main": [[{"node": "Responder 200", "type": "main", "index": 0}]]
        },
    },
    "settings": {"executionOrder": "v1"},
    "staticData": None,
    "tags": [],
    "triggerCount": 1,
    "updatedAt": "2026-03-21T13:00:00.000Z",
    "versionId": "1",
    "meta": {"templateId": "contact_form", "templateName": "Contacto Landing Sural"},
}

conn = sqlite3.connect(N8N_DB)
cursor = conn.cursor()

cursor.execute("SELECT MAX(id) FROM workflow")
max_id = cursor.fetchone()[0] or 0
new_id = max_id + 1

cursor.execute("SELECT COUNT(*) FROM workflow")
count = cursor.fetchone()[0]
new_order = count + 1

workflow_json = json.dumps(workflow)

cursor.execute(
    """
    INSERT INTO workflow (id, name, nodes, connections, active, createdAt, updatedAt, settings, staticData, triggerCount, versionId, tags, meta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        new_id,
        workflow["name"],
        workflow_json,
        json.dumps(workflow["connections"]),
        0,
        "2026-03-21T13:00:00.000Z",
        "2026-03-21T13:00:00.000Z",
        json.dumps(workflow["settings"]),
        None,
        1,
        "1",
        "[]",
        json.dumps(workflow["meta"]),
    ),
)

conn.commit()
print(f"Workflow 'Contacto Landing Sural' inserted with id={new_id}")
conn.close()
