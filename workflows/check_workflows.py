#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== workflow_entity ===")
cur.execute("SELECT id, name, active, versionId, activeVersionId FROM workflow_entity")
for r in cur.fetchall():
    print(f"  {r}")

print("\n=== workflow_published_version ===")
cur.execute("SELECT * FROM workflow_published_version")
for r in cur.fetchall():
    print(f"  {r}")

print("\n=== webhook_entity ===")
cur.execute("SELECT * FROM webhook_entity")
for r in cur.fetchall():
    print(f"  {r}")

print("\n=== project ===")
cur.execute("SELECT * FROM project")
for r in cur.fetchall():
    print(f"  {r}")

conn.close()
