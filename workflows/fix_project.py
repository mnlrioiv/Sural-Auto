import sqlite3

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()
cur.execute(
    "UPDATE project SET creatorId = 'b66a80536fc4c77b67af39c9c00db4b7' WHERE id = 'Bmv03objZqb84raI'"
)
db.commit()
print("Updated:", cur.rowcount)
db.close()
