import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

for wf_id in ["zYOskqzKJNvMmayO", "MZydQWJjP9Fe5ZoS", "NbZql7puc6e3Kygt"]:
    cur.execute("SELECT name, nodes FROM workflow_entity WHERE id = ?", (wf_id,))
    row = cur.fetchone()
    if row:
        nodes = json.loads(row[1])
        print(f"\n=== {row[0]} ===")
        for n in nodes:
            if "webhook" in n.get("type", "").lower():
                print(f"  Node: {n['name']}")
                print(f"  Type: {n['type']}")
                print(f"  TypeVersion: {n.get('typeVersion')}")
                print(f"  Params: {json.dumps(n.get('parameters', {}), indent=4)}")

db.close()
