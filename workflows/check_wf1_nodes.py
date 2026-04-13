#!/usr/bin/env python3
import sqlite3
import json

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT nodes FROM workflow_entity WHERE id = 1")
nodes = json.loads(cur.fetchone()[0])
for n in nodes:
    print(f"Workflow 1 webhook: type={n.get('type')}, name={n.get('name')}")

conn.close()
