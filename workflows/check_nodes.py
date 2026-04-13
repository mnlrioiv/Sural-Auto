#!/usr/bin/env python3
import sqlite3

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("SELECT name, type FROM installed_nodes")
nodes = cur.fetchall()
print("Installed nodes:")
for n in sorted(nodes):
    if any(
        x in n[0].lower()
        for x in [
            "webhook",
            "schedule",
            "email",
            "http",
            "code",
            "if",
            "set",
            "delay",
            "respond",
            "slack",
            "telegram",
        ]
    ):
        print(f"  {n[0]}: {n[1]}")

print("\n--- All nodes (webhook-related) ---")
for n in sorted(nodes):
    if "webhook" in n[0].lower() or "trigger" in n[0].lower():
        print(f"  {n[0]}: {n[1]}")

conn.close()
