#!/usr/bin/env python3
import sqlite3
import secrets

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT id, email, firstName, settings FROM user")
for r in cur.fetchall():
    print(f"User: {r}")

api_key = "sk_n8n_" + secrets.token_hex(24)
user_id = "f8898d02-cb05-45c1-ac86-2a46607f93cf"

cur.execute(
    """
    INSERT INTO user_api_keys (id, userId, label, apiKey, createdAt, updatedAt, scopes, audience)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
    (
        secrets.token_hex(16),
        user_id,
        "CLI Key",
        api_key,
        "2026-03-21T14:00:00.000Z",
        "2026-03-21T14:00:00.000Z",
        '["workflow:read","workflow:write","credential:read","credential:write"]',
        "",
    ),
)

conn.commit()
print(f"\nCreated API key: {api_key}")

cur.execute("SELECT * FROM user_api_keys")
for r in cur.fetchall():
    print(f"API Key: {r}")

conn.close()
