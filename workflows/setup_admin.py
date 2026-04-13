#!/usr/bin/env python3
import sqlite3
import secrets
import hashlib

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute(
    "UPDATE settings SET value='false' WHERE key='userManagement.isInstanceOwnerSetUp'"
)

user_id = "f8898d02-cb05-45c1-ac86-2a46607f93cf"
cur.execute("DELETE FROM user WHERE id = ?", (user_id,))

password_hash = hashlib.sha256("SuralAdmin2026!".encode()).hexdigest()
cur.execute(
    """
    INSERT INTO user (id, email, firstName, lastName, password, personalizationAnswers, createdAt, updatedAt, settings, disabled, mfaEnabled, mfaSecret, mfaRecoveryCodes, lastActiveAt, roleSlug)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        user_id,
        "admin@sural.com",
        "Admin",
        "Sural",
        password_hash,
        "{}",
        "2026-03-21T00:00:00.000Z",
        "2026-03-21T14:00:00.000Z",
        '{"userActivated":true}',
        0,
        0,
        "",
        "",
        "2026-03-21T14:00:00.000Z",
        "global:owner",
    ),
)

api_key = "sk_n8n_" + secrets.token_hex(24)
cur.execute(
    """
    INSERT INTO user_api_keys (id, userId, label, apiKey, createdAt, updatedAt, scopes, audience)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        secrets.token_hex(16),
        user_id,
        "Admin Key",
        api_key,
        "2026-03-21T14:00:00.000Z",
        "2026-03-21T14:00:00.000Z",
        '["*"]',
        "",
    ),
)

cur.execute(
    """
    INSERT OR REPLACE INTO project_relation (projectId, userId, role, createdAt)
    VALUES (?, ?, ?, ?)
""",
    ("Bmv03objZqb84raI", user_id, "owner", "2026-03-21T00:00:00.000Z"),
)

conn.commit()
print(f"User created: admin@sural.com / SuralAdmin2026!")
print(f"API Key: {api_key}")

cur.execute("SELECT id, email, firstName, roleSlug, settings FROM user")
for r in cur.fetchall():
    print(f"User: {r}")

conn.close()
