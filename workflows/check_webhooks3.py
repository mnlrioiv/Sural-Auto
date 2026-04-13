import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

wf_ids = [
    "zYOskqzKJNvMmayO",
    "MZydQWJjP9Fe5ZoS",
    "NbZql7puc6e3Kygt",
    "xJ9DEY4rYscYU5vw",
]
wf_names = {}
cur.execute("SELECT id, name FROM workflow_entity")
for r in cur.fetchall():
    wf_names[r[0]] = r[1]

for wf_id in wf_ids:
    cur.execute("SELECT nodes FROM workflow_entity WHERE id = ?", (wf_id,))
    row = cur.fetchone()
    if row:
        nodes = json.loads(row[0])
        webhooks = [n for n in nodes if "webhook" in n.get("type", "").lower()]
        print(
            f"{wf_names.get(wf_id, '?')}: webhooks in nodes = {[w['name'] for w in webhooks]}"
        )

        cur.execute(
            "SELECT COUNT(*) FROM webhook_entity WHERE workflowId = ?", (wf_id,)
        )
        count = cur.fetchone()[0]
        print(f"  -> registered in webhook_entity: {count}")
db.close()
