#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
uuids = ["WP8xAbM1k2i5TnHd", "Rc7o7A3uiDG9rL5f", "rX4uv2b2WnDRMWMX", "NVUMMB6Ho2KhUH0G"]
conn = sqlite3.connect(DB)
cur = conn.cursor()

import json

for uuid in uuids:
    cur.execute("SELECT nodes FROM workflow_entity WHERE id = ?", (uuid,))
    row = cur.fetchone()
    if row:
        nodes = json.loads(row[0])
        for n in nodes:
            if n.get("type") == "n8n-nodes-base.if":
                print(
                    f"{uuid} - {n['name']}: {json.dumps(n['parameters'].get('conditions', {}), indent=2)[:500]}"
                )
conn.close()
