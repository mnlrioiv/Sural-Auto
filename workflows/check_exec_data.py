import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT executionId, workflowId, data FROM execution_data ORDER BY workflowId DESC LIMIT 5"
)
for r in cur.fetchall():
    print(f"exec={str(r[0])[:8]} wf={str(r[1])[:8]}")
    # data is a JSON blob, print first 500 chars
    data = r[2]
    if data:
        import json

        try:
            d = json.loads(data)
            print(f"  data keys: {list(d.keys())}")
            if "resultData" in d:
                rd = d["resultData"]
                if "error" in rd:
                    print(f"  ERROR: {str(rd['error'])[:300]}")
                if "lastNodeExecuted" in rd:
                    print(f"  lastNode: {rd['lastNodeExecuted']}")
        except:
            print(f"  raw: {str(data)[:200]}")
db.close()
