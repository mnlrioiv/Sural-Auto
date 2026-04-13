#!/usr/bin/env python3
import json
import subprocess

base = "/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-nodes-base@file+packages+nodes-base_@aws-sdk+credential-providers@3.808.0_asn1.js@5_8da18263ca0574b0db58d4fefd8173ce/node_modules/n8n-nodes-base/dist"

nodes_to_check = [
    "Webhook/Webhook.node.json",
    "Code/Code.node.json",
    "EmailSend/EmailSend.node.json",
    "HttpRequest/HttpRequest.node.json",
    "If/If.node.json",
    "Set/Set.node.json",
    "Delay/Delay.node.json",
    "RespondToWebhook/RespondToWebhook.node.json",
    "ScheduleTrigger/ScheduleTrigger.node.json",
]

for node_path in nodes_to_check:
    full_path = f"{base}/nodes/{node_path}"
    try:
        result = subprocess.run(
            ["docker", "exec", "automation-n8n-1", "cat", full_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            name = data.get("name", "N/A")
            display = data.get("displayName", "N/A")
            version = data.get("version", "N/A")
            print(
                f"{node_path.split('/')[0]}: name={name}, display={display}, version={version}"
            )
    except Exception as e:
        print(f"{node_path}: error - {e}")
