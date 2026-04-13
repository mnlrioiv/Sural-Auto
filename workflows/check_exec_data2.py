import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute("PRAGMA table_info(execution_data)")
cols = [r[1] for r in cur.fetchall()]
print("execution_data cols:", cols)
cur.execute(
    "SELECT executionId, data FROM execution_data ORDER BY executionId DESC LIMIT 3"
)
for r in cur.fetchall():
    eid = str(r[0])
    data = r[1]
    if data:
        try:
            d = json.loads(data)
            print(f"\nexec={eid[:8]}: keys={list(d.keys())}")
            if "resultData" in d:
                rd = d["resultData"]
                if "error" in rd:
                    print(f"  ERROR: {str(rd['error'])[:400]}")
                if "lastNodeExecuted" in rd:
                    print(f"  lastNode: {rd['lastNodeExecuted']}")
            if "error" in d:
                print(f"  TOP-LEVEL ERROR: {str(d['error'])[:400]}")
        except Exception as e:
            print(f"  parse error: {e}")
            print(f"  raw: {str(data)[:200]}")
db.close()
