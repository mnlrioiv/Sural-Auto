#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT id, name, active, versionId, activeVersionId FROM workflow_entity")
for r in cur.fetchall():
    print(f"  Workflow {r[0]}: {r[1]} (active={r[2]}, ver={r[3]}, activeVer={r[4]})")

conn.close()
