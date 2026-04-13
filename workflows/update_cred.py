import sqlite3
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

new_encrypted = "U2FsdGVkX1+FhWMItTmB5X4mI8pbtFOa4Y+GH6dg7651KWGA74xcHqQt4hybkHTI/xwvEWEDle4OJ4k4qeYF9QjhSchWo+X8j8GasH2dM4kTZ2VhIC2DeIvEB03f7NXqpyw7hRU1s+vCfmzqRIBm3dsIvZoodp5vVEW2p0aAlpI="

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
cur.execute(
    "UPDATE credentials_entity SET data = ?, updatedAt = ? WHERE id = 'ae1a4d81-c7a6-4655-9cc7-22df2db12393'",
    (new_encrypted, now),
)
print(f"Updated: {cur.rowcount} rows")

db.commit()
db.close()
print("Done!")
