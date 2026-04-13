#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DELETE FROM webhook_entity WHERE workflowId = 1")

cur.execute(
    """
    INSERT INTO webhook_entity (workflowId, webhookPath, method, node, webhookId, pathLength)
    VALUES (?, ?, ?, ?, ?, ?)
""",
    (1, "contacto-sural", "POST", "node-webhook-1", "contacto-sural", 14),
)

conn.commit()
print("Webhook registered")
cur.execute("SELECT * FROM webhook_entity")
print(cur.fetchall())
conn.close()
