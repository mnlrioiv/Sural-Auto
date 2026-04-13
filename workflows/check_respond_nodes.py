import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("SELECT id, name, nodes FROM workflow_entity")
for r in cur.fetchall():
    nodes = json.loads(r[2])
    for n in nodes:
        if "respond" in n.get("type", "").lower():
            print(f"\n=== {r[1]} - {n['name']} ===")
            print(json.dumps(n.get("parameters", {}), indent=2))
db.close()
