import sqlite3, uuid
from datetime import datetime, timezone

db = sqlite3.connect("/opt/sural/automation/n8n_data/database.sqlite")
cur = db.cursor()

encrypted_cred = "U2FsdGVkX18HExViDB1uSWGSecNbAX4qfWRqGCkn21GBTkepS1X/pmP+zi6HaDHGdpRO1qaHyGyMSmIwGAllJ4q1YvqjOQnBIYw4R4/9bKCRdXPgmuUjYtDMV+ajLdEgcgoZ4nLV7+pioc0SDOR6JGPXeWEd/Q9sZTxtiNIaiI03ZLv3sAfOgoUk2o1rngK2FK+LQzOlcwHO7TQgLEjlGA=="

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
cred_id = str(uuid.uuid4())

cur.execute(
    "INSERT INTO credentials_entity (id, name, type, data, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?, ?)",
    (cred_id, "SMTP Sural", "smtp", encrypted_cred, now, now),
)
print(f"Created credential: {cred_id}")

proj_id = "Bmv03objZqb84raI"
cur.execute(
    "INSERT INTO shared_credentials (credentialsId, projectId, role, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)",
    (cred_id, proj_id, "credential:owner", now, now),
)
print(f"Shared credential with project")

db.commit()
db.close()
print("\nDone!")
