#!/usr/bin/env python3
import subprocess, json, glob, os

base = "/usr/local/lib/node_modules/n8n/node_modules/.pnpm"
pattern = f"{base}/n8n-nodes-base*/node_modules/n8n-nodes-base/dist/nodes/*/*.node.json"

nodes = {}
for f in glob.glob(pattern):
    try:
        data = json.load(open(f, "rb"))
        name = data.get("name", "N/A")
        display = data.get("displayName", "N/A")
        version = data.get("version", "N/A")
        short = os.path.basename(os.path.dirname(f))
        if short not in nodes:
            nodes[short] = {"name": name, "display": display, "version": version}
    except:
        pass

for short, info in sorted(nodes.items()):
    print(
        f"  {short}: {info['name']} (display: {info['display']}, version: {info['version']})"
    )
