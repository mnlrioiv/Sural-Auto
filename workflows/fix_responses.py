import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

responses = {
    "566a8a51": {
        "resp1": "={{ JSON.stringify({status: 'ok', score: $json.lead_score}) }}",
        "resp2": "={{ JSON.stringify({status: 'ok'}) }}",
    },
    "ab0df327": {
        "resp2a": "={{ JSON.stringify({status: 'ok', ticket_id: $json.ticket_id, priority: $json.priority}) }}",
        "resp2b": "={{ JSON.stringify({status: 'ok', ticket_id: $json.ticket_id}) }}",
    },
    "68051057": {"resp3": "={{ JSON.stringify({status: 'ok', sequence: 'started'}) }}"},
}

cur.execute("SELECT id, name, nodes FROM workflow_entity")
for r in cur.fetchall():
    wf_id = r[0]
    wf_short = wf_id[:8]
    nodes = json.loads(r[2])

    if wf_short in responses:
        modified = False
        for node in nodes:
            node_id = node.get("id")
            if node_id in responses[wf_short]:
                old_val = node["parameters"]["responseBody"]
                node["parameters"]["responseBody"] = responses[wf_short][node_id]
                modified = True
                print(
                    f"  Updated {node['name']} in {r[1]}: {old_val[:40]}... -> {responses[wf_short][node_id][:40]}..."
                )

        if modified:
            cur.execute(
                "UPDATE workflow_entity SET nodes = ? WHERE id = ?",
                (json.dumps(nodes), wf_id),
            )

db.commit()
db.close()
print("\nDone!")
