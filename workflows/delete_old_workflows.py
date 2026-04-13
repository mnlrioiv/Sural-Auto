#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

tables = {
    "workflow_entity": "id",
    "workflow_published_version": "workflowId",
    "workflow_history": "workflowId",
    "webhook_entity": "workflowId",
    "shared_workflow": "workflowId",
}

for table, id_col in tables.items():
    try:
        cur.execute(
            f"DELETE FROM {table} WHERE {id_col} IN ('1', '2', '3', '4', '5', '6')"
        )
        print(f"Deleted {cur.rowcount} rows from {table}")
    except Exception as e:
        print(f"Error on {table}: {e}")

conn.commit()

cur.execute("SELECT id, name FROM workflow_entity")
for r in cur.fetchall():
    print(f"  Workflow {r[0]}: {r[1]}")

conn.close()
print("\nDone")
