import sqlite3, json, uuid
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

# User already exists: b66a80536fc4c77b67af39c9c00db4b7
# Set its password
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
password_hash = "$2a$10$nDIzLMSow1Yoo0f0EkGWOeCKmUGvlb6OHHLRBnu1JK0UPMPZ2.z4K"

cur.execute(
    "UPDATE user SET password = ? WHERE email = 'admin@sural.com'", (password_hash,)
)
print(f"Updated password for admin@sural.com ({cur.rowcount} rows)")

# Check settings
cur.execute("SELECT key, value FROM settings WHERE key = 'isInstanceOwnerSetUp'")
row = cur.fetchone()
print(f"isInstanceOwnerSetUp: {row[1] if row else 'NOT FOUND'}")

if not row:
    cur.execute(
        "INSERT INTO settings (key, value, loadOnStartup) VALUES ('isInstanceOwnerSetUp', 'true', 1)"
    )
    print("Inserted isInstanceOwnerSetUp = true")
elif row[1] != "true":
    cur.execute("UPDATE settings SET value = 'true' WHERE key = 'isInstanceOwnerSetUp'")
    print("Updated isInstanceOwnerSetUp = true")

db.commit()
db.close()
print(
    "\nDone! Now restart n8n and login at http://158.69.59.178:5678 with admin@sural.com / Sural2026!"
)
