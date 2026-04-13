import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute(
    "SELECT name, nodes, connections FROM workflow_entity WHERE id IN ('zYOskqzKJNvMmayO', 'MZydQWJjP9Fe5ZoS')"
)
for row in cur.fetchall():
    name = row[0]
    nodes = json.loads(row[1])
    connections = json.loads(row[2])
    print(f"\n=== {name} ===")
    print(f"Nodes ({len(nodes)}):")
    for n in nodes:
        t = n["type"]
        p = n.get("parameters", {})
        if "code" in t.lower() or "respond" in t.lower() or "email" in t.lower():
            safe_p = {
                k: (v if len(str(v)) < 200 else str(v)[:200] + "...")
                for k, v in p.items()
            }
            print(f"  {n['name']} ({t}): {json.dumps(safe_p)}")

    print(f"Connections:")
    print(json.dumps(connections, indent=2))

db.close()
