import sqlite3, json

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

cur.execute("PRAGMA table_info(user)")
cols = [r[1] for r in cur.fetchall()]
print("user columns:", cols)
cur.execute(f"SELECT {','.join(cols)} FROM user")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(
        f"  email={d.get('email')} isOwner={d.get('isOwner')} isInstanceOwner={d.get('isInstanceOwner')} id={d.get('id', '')[:20]}"
    )

print("\n=== settings ===")
cur.execute("SELECT name, value FROM settings")
for r in cur.fetchall():
    print(f"  {r[0]} = {str(r[1])[:80]}")

print("\n=== api keys ===")
cur.execute("SELECT id, name, userId, key FROM user_api_keys")
for r in cur.fetchall():
    print(f"  id={r[0][:8]} name={r[1]} userId={r[2][:8]}")

db.close()
