#!/usr/bin/env python3
import sqlite3
import json

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

webhooks = {
    2: {"path": "lead-calificacion", "webhook_id": "lead-calificacion"},
    3: {"path": "follow-up-semanal", "webhook_id": "follow-up-semanal"},
    4: {"path": "generar-presupuesto", "webhook_id": "generar-presupuesto"},
    5: {"path": "soporte-ticket", "webhook_id": "soporte-ticket"},
    6: {"path": "marketing-new-lead", "webhook_id": "marketing-new-lead"},
}

cur.execute("UPDATE workflow_entity SET active = 1 WHERE id > 1")

for wf_id, wh in webhooks.items():
    cur.execute("DELETE FROM webhook_entity WHERE workflowId = ?", (wf_id,))
    cur.execute(
        """
        INSERT INTO webhook_entity (workflowId, webhookPath, method, node, webhookId, pathLength)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            wf_id,
            wh["path"],
            "POST",
            "webhook-trigger",
            wh["webhook_id"],
            len(wh["path"]),
        ),
    )

conn.commit()

cur.execute("SELECT id, name, active, versionId FROM workflow_entity")
for row in cur.fetchall():
    print(f"  Workflow {row[0]}: {row[1]} (active={row[2]}, version={row[3]})")

cur.execute("SELECT * FROM webhook_entity")
print("\nWebhooks:")
for row in cur.fetchall():
    print(f"  {row}")

conn.close()
print("\nAll workflows activated and webhooks registered!")
