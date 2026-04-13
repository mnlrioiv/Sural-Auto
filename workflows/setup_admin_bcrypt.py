#!/usr/bin/env python3
import sqlite3
import secrets

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

password_hash = "$2a$10$oBKRUPjS0gHEzLxrWhLt1ewvWHppi4d.1jFdq33I1AJjCKTTF1MOe"
user_id = secrets.token_hex(16)

cur.execute("DELETE FROM user")
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
        "2026-03-21T14:00:00.000Z",
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

cur.execute(
    """
    INSERT INTO project_relation (projectId, userId, role, createdAt)
    VALUES (?, ?, ?, ?)
""",
    ("Bmv03objZqb84raI", user_id, "owner", "2026-03-21T14:00:00.000Z"),
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
        "Admin API Key",
        api_key,
        "2026-03-21T14:00:00.000Z",
        "2026-03-21T14:00:00.000Z",
        '["*"]',
        "",
    ),
)

conn.commit()
print(f"User created with bcrypt hash")
print(f"User ID: {user_id}")
print(f"API Key: {api_key}")

conn.close()
