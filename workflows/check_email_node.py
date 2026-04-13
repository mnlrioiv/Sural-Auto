import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT nodes FROM workflow_entity WHERE id='566a8a51-79f5-434c-a412-e280398bb2f3'"
)
row = cur.fetchone()
nodes = json.loads(row[0])
for n in nodes:
    if "email" in n.get("type", "").lower():
        print(json.dumps(n, indent=2))
db.close()
