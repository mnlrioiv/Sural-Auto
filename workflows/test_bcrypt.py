#!/usr/bin/env python3
import subprocess
import secrets
import sys

result = subprocess.run(
    [
        "node",
        "-e",
        """
const bcrypt = require('/usr/local/lib/node_modules/n8n/node_modules/.pnpm/bcryptjs*/node_modules/bcryptjs/lib/index.js');
""",
    ],
    capture_output=True,
    text=True,
    timeout=5,
)
print(result.stdout, result.stderr)
