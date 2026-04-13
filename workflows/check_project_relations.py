import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

# Check project_relation
cur.execute("PRAGMA table_info(project_relation)")
cols = [r[1] for r in cur.fetchall()]
print("project_relation cols:", cols)

cur.execute(f"SELECT {','.join(cols)} FROM project_relation")
for r in cur.fetchall():
    d = dict(zip(cols, r))
    print(f"  {d}")

# Check project_user
cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%project%user%'"
)
for r in cur.fetchall():
    print(f"Table: {r[0]}")

# Check all project-related tables
for tbl in ["project_relation", "project_user", "project_role"]:
    try:
        cur.execute(f"SELECT * FROM {tbl}")
        cols = [d[0] for d in cur.description]
        print(f"\n{tbl}: {cur.fetchall()}")
    except:
        print(f"\n{tbl}: table not found or empty")

db.close()
