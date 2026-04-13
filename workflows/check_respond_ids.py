import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("SELECT id, name, nodes FROM workflow_entity")
for r in cur.fetchall():
    wf_id = r[0]
    nodes = json.loads(r[2])

    for node in nodes:
        if "respond" in node.get("type", "").lower():
            print(f"wf={wf_id[:8]} node_id={node.get('id')} name={node['name']}")
            print(f"  params: {json.dumps(node.get('parameters', {}))}")

db.close()
