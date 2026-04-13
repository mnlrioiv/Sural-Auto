import sqlite3
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

new_encrypted = "U2FsdGVkX1+Wr6ABFAGBUIEWUvz23hMNPATdnPaeohvFTjxc3lT6l1/eoCxej39uOqPlSOTV2/Cr54zWGlm4oHEc/tAQuNdVJ87U2yqzGCUlPTM97UeAa6qQxaocWTtPPlkTI8XX8HG/PLkb7ias8i3mXadNYgaIlVNo9qHioW2W287JJZiPGPCVOJSRnGt8"

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
cur.execute(
    "UPDATE credentials_entity SET data = ?, updatedAt = ? WHERE id = 'ae1a4d81-c7a6-4655-9cc7-22df2db12393'",
    (new_encrypted, now),
)
print(f"Updated: {cur.rowcount} rows")

db.commit()
db.close()
print("Done!")
