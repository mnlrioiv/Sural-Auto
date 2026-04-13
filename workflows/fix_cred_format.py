#!/usr/bin/env python3
import sqlite3, json, sys

DB = "/opt/sural/automation/n8n_data/database.sqlite"

workflows = [
    "566a8a51-79f5-434c-a412-e280398bb2f3",
    "ab0df327-9141-4372-960f-e10f485b8711",
    "68051057-a182-420b-8889-985006ca77a0",
    "2fdbc69b-bdc3-442a-b549-26c16f1c169e",
]


def fix_credentials_in_nodes(nodes_json):
    nodes = json.loads(nodes_json)
    for node in nodes:
        if node.get("credentials"):
            new_creds = {}
            for cred_type, cred_val in node["credentials"].items():
                if isinstance(cred_val, str):
                    new_creds[cred_type] = {"id": cred_val}
                elif isinstance(cred_val, dict) and "id" not in cred_val:
                    new_creds[cred_type] = {"id": cred_val.get("name", "")}
                else:
                    new_creds[cred_type] = cred_val
            node["credentials"] = new_creds
    return json.dumps(nodes, ensure_ascii=False)


conn = sqlite3.connect(DB)
cur = conn.cursor()

for wf_id in workflows:
    # Update workflow_entity
    cur.execute("SELECT id, name, nodes FROM workflow_entity WHERE id=?", (wf_id,))
    row = cur.fetchone()
    if row:
        fixed = fix_credentials_in_nodes(row[2])
        cur.execute("UPDATE workflow_entity SET nodes=? WHERE id=?", (fixed, wf_id))
        print(f"Updated workflow_entity: {row[1]} ({wf_id[:8]})")

    # Update workflow_history for all versions of this workflow
    cur.execute(
        "SELECT versionId, nodes FROM workflow_history WHERE workflowId=?", (wf_id,)
    )
    for hist_row in cur.fetchall():
        vid, hist_nodes = hist_row
        if hist_nodes:
            fixed_hist = fix_credentials_in_nodes(hist_nodes)
            cur.execute(
                "UPDATE workflow_history SET nodes=? WHERE versionId=?",
                (fixed_hist, vid),
            )
            print(f"  Updated workflow_history: {vid[:8]}...")

conn.commit()
print("Done!")
