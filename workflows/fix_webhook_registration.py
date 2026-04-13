import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

webhooks_to_add = [
    ("zYOskqzKJNvMmayO", "lead-calificacion", "POST", "Webhook Trigger"),
    ("MZydQWJjP9Fe5ZoS", "soporte-ticket", "POST", "Webhook Trigger"),
]

for wf_id, path, method, node in webhooks_to_add:
    cur.execute(
        "SELECT COUNT(*) FROM webhook_entity WHERE workflowId = ? AND webhookPath = ?",
        (wf_id, path),
    )
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO webhook_entity (workflowId, webhookPath, method, node) VALUES (?, ?, ?, ?)",
            (wf_id, path, method, node),
        )
        print(f"Added webhook: {path} for workflow {wf_id[:8]}")
    else:
        print(f"Webhook {path} already exists")

db.commit()
print("\nDone. Now deactivate and reactivate workflows to force webhook registration.")
db.close()
