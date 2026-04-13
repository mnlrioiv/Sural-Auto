#!/usr/bin/env python3
"""
Webhook server para el formulario de contacto de Sural.
Recibe POST requests y las reenvía a n8n y Chatwoot.
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

PORT = 5679
N8N_WEBHOOK = "http://localhost:5678/webhook/contacto-sural"
CHATWOOT_API = os.environ.get("CHATWOOT_API_URL", "http://localhost:3001")
CHATWOOT_TOKEN = os.environ.get("CHATWOOT_API_TOKEN", "")


class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info(
            "%s - - [%s] %s"
            % (self.address_string(), self.log_date_time_string(), format % args)
        )

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/webhook/contacto":
            self.send_json({"error": "Not found"}, 404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        logger.info(
            f"Received lead: {data.get('nombre', 'N/A')} - {data.get('email', 'N/A')}"
        )

        data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        data["source"] = "landing_page"

        results = {}

        try:
            req = urllib.request.Request(
                N8N_WEBHOOK,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
                timeout=10,
            )
            with urllib.request.urlopen(req) as resp:
                results["n8n"] = {"status": resp.status, "body": resp.read().decode()}
                logger.info(f"n8n responded: {resp.status}")
        except urllib.error.HTTPError as e:
            results["n8n"] = {"status": e.code, "error": e.read().decode()}
            logger.warning(f"n8n HTTP error: {e.code}")
        except urllib.error.URLError as e:
            results["n8n"] = {"error": str(e.reason)}
            logger.warning(f"n8n connection error: {e.reason}")
        except Exception as e:
            results["n8n"] = {"error": str(e)}
            logger.error(f"n8n error: {e}")

        if CHATWOOT_TOKEN:
            try:
                conv_data = json.dumps(
                    {
                        "inbox_id": 1,
                        "contact": {
                            "name": data.get("nombre", ""),
                            "email": data.get("email", ""),
                            "phone_number": data.get("telefono", ""),
                        },
                        "message": f"Nuevo lead desde landing page\n\nNombre: {data.get('nombre', '')}\nEmpresa: {data.get('empresa', '')}\nEmail: {data.get('email', '')}\nTeléfono: {data.get('telefono', '')}\nInterés: {data.get('interes', '')}\nMensaje: {data.get('mensaje', '')}",
                    }
                ).encode("utf-8")
                req2 = urllib.request.Request(
                    f"{CHATWOOT_API}/api/v1/conversations",
                    data=conv_data,
                    headers={
                        "Content-Type": "application/json",
                        "api_access_token": CHATWOOT_TOKEN,
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req2) as resp:
                    results["chatwoot"] = {"status": resp.status}
                    logger.info(f"Chatwoot responded: {resp.status}")
            except Exception as e:
                results["chatwoot"] = {"error": str(e)}
                logger.warning(f"Chatwoot error: {e}")

        self.send_json(
            {
                "status": "ok",
                "message": "Consulta recibida. Te contactaremos pronto.",
                "received": True,
            }
        )
        logger.info(f"Webhook processed for {data.get('email', 'unknown')}")


if __name__ == "__main__":
    os.makedirs("/opt/sural/logs", exist_ok=True)
    with socketserver.TCPServer(("", PORT), WebhookHandler) as httpd:
        logger.info(f"Webhook server listening on port {PORT}")
        httpd.serve_forever()
