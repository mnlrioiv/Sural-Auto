#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

for wf_id in [2, 3, 4, 5, 6]:
    cur.execute(
        "UPDATE workflow_entity SET activeVersionId = ? WHERE id = ?",
        (str(wf_id), wf_id),
    )

conn.commit()

cur.execute("SELECT id, name, active, versionId, activeVersionId FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r}")

conn.close()
print("Fixed activeVersionId for all workflows!")
