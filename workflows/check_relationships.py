#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("PRAGMA table_info(workflow_entity)")
cols = {r[1]: r[2] for r in cur.fetchall()}
print("workflow_entity columns:", cols)

cur.execute("PRAGMA table_info(project)")
cols2 = {r[1]: r[2] for r in cur.fetchall()}
print("project columns:", cols2)

cur.execute("SELECT * FROM shared_workflow")
print("\nshared_workflow:")
for r in cur.fetchall():
    print(f"  {r}")

cur.execute("SELECT * FROM project")
print("\nproject:")
for r in cur.fetchall():
    print(f"  {r}")

conn.close()
