import sqlite3, json, uuid
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("PRAGMA table_info(settings)")
cols = [r[1] for r in cur.fetchall()]
print("settings cols:", cols)
cur.execute(f"SELECT {','.join(cols)} FROM settings")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(f"  {d}")

db.close()
