import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

print("=== All webhook_entity rows ===")
cur.execute(
    "SELECT workflowId, webhookPath, method, node, webhookId, pathLength FROM webhook_entity"
)
for r in cur.fetchall():
    print(
        f"  wfId={r[0]} path={r[1]} method={r[2]} node={r[3]} webhookId={r[4]} pathLen={r[5]}"
    )

print("\n=== Check Marketing Nurturing nodes (working) ===")
cur.execute(
    "SELECT nodes, connections FROM workflow_entity WHERE id = 'NbZql7puc6e3Kygt'"
)
row = cur.fetchone()
if row:
    nodes = json.loads(row[0])
    for n in nodes:
        if (
            "webhook" in n.get("type", "").lower()
            or "webhook" in n.get("name", "").lower()
        ):
            print(
                f"  {n['name']}: type={n['type']} webhookId={n.get('parameters', {}).get('webhookId', '')}"
            )

print("\n=== Check Lead Reception nodes (not working) ===")
cur.execute("SELECT nodes FROM workflow_entity WHERE id = 'zYOskqzKJNvMmayO'")
row = cur.fetchone()
if row:
    nodes = json.loads(row[0])
    for n in nodes:
        if (
            "webhook" in n.get("type", "").lower()
            or "webhook" in n.get("name", "").lower()
        ):
            print(
                f"  {n['name']}: type={n['type']} webhookId={n.get('parameters', {}).get('webhookId', '')}"
            )

db.close()
