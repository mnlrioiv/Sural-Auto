#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
uuids = ["WP8xAbM1k2i5TnHd", "Rc7o7A3uiDG9rL5f", "rX4uv2b2WnDRMWMX", "NVUMMB6Ho2KhUH0G"]
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("Before delete:")
cur.execute("SELECT id, name FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

for table in [
    "workflow_entity",
    "workflow_published_version",
    "workflow_history",
    "webhook_entity",
    "shared_workflow",
]:
    cur.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    id_col = None
    for c in cols:
        if c in ["id", "workflowId"]:
            id_col = c
            break
    if id_col:
        placeholders = ",".join(["?"] * len(uuids))
        cur.execute(f"DELETE FROM {table} WHERE {id_col} IN ({placeholders})", uuids)
        print(f"Deleted {cur.rowcount} from {table} ({id_col})")
    else:
        print(f"No id column found in {table}: {cols}")

conn.commit()

print("\nAfter delete:")
cur.execute("SELECT id, name FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")
conn.close()
