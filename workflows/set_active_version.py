import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("""
    UPDATE workflow_entity 
    SET activeVersionId = versionId
    WHERE active = 1 AND activeVersionId IS NULL
""")
print(f"Updated {cur.rowcount} workflows")

cur.execute("SELECT id, name, versionId, activeVersionId FROM workflow_entity")
for r in cur.fetchall():
    print(
        f"  {r[0][:8]} | {r[1]} | vid={r[2][:8]} | activeVid={r[3][:8] if r[3] else 'NULL'}"
    )

db.commit()
db.close()
print("\nDone! Restart n8n to activate workflows.")
