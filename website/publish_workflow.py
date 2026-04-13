#!/usr/bin/env python3
import sqlite3
import json

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

now = "2026-03-21T13:00:00.000Z"

cur.execute("SELECT versionId FROM workflow_entity WHERE id = 1")
row = cur.fetchone()
version_id = row[0] if row else "1"

cur.execute(
    """
    INSERT OR REPLACE INTO workflow_published_version (workflowId, publishedVersionId, createdAt)
    VALUES (1, ?, ?)
""",
    (version_id, now),
)

cur.execute(
    """
    UPDATE workflow_entity SET activeVersionId = ? WHERE id = 1
""",
    (version_id,),
)

conn.commit()

cur.execute(
    "SELECT id, name, active, versionId, activeVersionId FROM workflow_entity WHERE id = 1"
)
print("Workflow:", cur.fetchall())

cur.execute("SELECT * FROM workflow_published_version")
print("Published versions:", cur.fetchall())

conn.close()
