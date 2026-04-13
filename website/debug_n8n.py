#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT * FROM project")
print("Projects:", cur.fetchall())

cur.execute("SELECT * FROM shared_workflow")
print("Shared workflows:", cur.fetchall())

cur.execute("SELECT id, name, active, versionId, activeVersionId FROM workflow_entity")
print("Workflows:", cur.fetchall())

cur.execute("SELECT * FROM workflow_published_version")
print("Published versions:", cur.fetchall())

conn.close()
