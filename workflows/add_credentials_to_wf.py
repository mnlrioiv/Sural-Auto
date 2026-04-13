import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

CRED_ID = "ae1a4d81-c7a6-4655-9cc7-22df2db12393"

cur.execute(
    "SELECT id, name, nodes FROM workflow_entity WHERE name IN ('Lead Reception & Qualification', 'Support Ticket Automation', 'Marketing Nurturing Sequence')"
)
for r in cur.fetchall():
    wf_id, name, nodes_json = r
    nodes = json.loads(nodes_json)

    modified = False
    for node in nodes:
        if (
            "emailSend" in node.get("type", "").lower()
            or "email" in node.get("type", "").lower()
        ):
            node["credentials"] = {"smtp": CRED_ID}
            modified = True
            print(f"  Added credential to {node['name']} in {name}")

    if modified:
        cur.execute(
            "UPDATE workflow_entity SET nodes = ? WHERE id = ?",
            (json.dumps(nodes), wf_id),
        )

db.commit()
db.close()
print("\nDone!")
