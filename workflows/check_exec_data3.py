import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "SELECT executionId, data FROM execution_data ORDER BY executionId DESC LIMIT 3"
)
for r in cur.fetchall():
    eid = str(r[0])
    data = r[1]
    if data:
        try:
            d = json.loads(data)
            # It's a list of objects with numeric keys
            data_dict = {int(k): v for k, v in d}
            print(f"\nexec={eid[:8]}:")
            for key in sorted(data_dict.keys()):
                val = data_dict[key]
                if key == 6:  # error index
                    print(f"  [6] ERROR: {str(val)[:500]}")
                elif key == 7:  # runData
                    print(f"  [7] runData: {str(val)[:200]}")
                elif key == 8:  # lastNodeExecuted
                    print(f"  [8] lastNode: {val}")
                else:
                    print(f"  [{key}]: {str(val)[:100]}")
        except Exception as e:
            print(f"  parse error: {e}")
db.close()
