#!/usr/bin/env python3
"""
Webhook handler for Sural - uses .env for configuration.
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
from datetime import datetime
import threading
import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "5679"))
CRM_URL = os.getenv("CRM_URL", "https://crm.sural.com.ar")
CRM_TOKEN = os.getenv("CRM_TOKEN", "")
TELEGRAM_BOT = os.getenv("TELEGRAM_BOT", "")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT", "")

ALLOWED_ORIGINS = ["https://sural.com.ar", "https://www.sural.com.ar"]


class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

    def get_cors_origin(self):
        origin = self.headers.get("Origin", "")
        if origin in ALLOWED_ORIGINS:
            return origin
        return None

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        cors_origin = self.get_cors_origin()
        if cors_origin:
            self.send_header("Access-Control-Allow-Origin", cors_origin)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        cors_origin = self.get_cors_origin()
        if cors_origin:
            self.send_header("Access-Control-Allow-Origin", cors_origin)
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
            self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_POST(self):
        if self.path not in ["/webhook/contacto", "/webhook/lead-calificacion"]:
            self.send_json({"error": "Not found"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body) if body else {}
        except:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        print(f"Lead: {data.get('nombre', 'N/A')} - {data.get('email', 'N/A')}")

        threading.Thread(target=self.send_to_crm, args=(data,), daemon=True).start()
        threading.Thread(
            target=self.send_to_telegram, args=(data,), daemon=True
        ).start()

        self.send_json(
            {
                "status": "ok",
                "message": "Consulta recibida. Te contactaremos pronto.",
                "received": True,
            }
        )

    def send_to_crm(self, data):
        if not CRM_TOKEN or not CRM_URL:
            print("CRM: Not configured")
            return
        try:
            req = urllib.request.Request(
                CRM_URL + "/rest/persons",
                data=json.dumps(
                    {
                        "nameFirstName": data.get("nombre", "Unknown"),
                        "emailsPrimaryEmail": data.get("email", ""),
                        "phonesPrimaryPhoneNumber": data.get("telefono", ""),
                    }
                ).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {CRM_TOKEN}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10):
                print("CRM: OK")
        except Exception as e:
            print(f"CRM error: {e}")

    def send_to_telegram(self, data):
        if not TELEGRAM_BOT or not TELEGRAM_CHAT:
            print("Telegram: Not configured")
            return
        try:
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
                data=json.dumps(
                    {
                        "chat_id": TELEGRAM_CHAT,
                        "text": f"🔔 *Nuevo Lead*\n\n*Nombre:* {data.get('nombre')}\n*Email:* {data.get('email')}\n*Tel:* {data.get('telefono', 'NS')}",
                        "parse_mode": "Markdown",
                    }
                ).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10):
                print("Telegram: OK")
        except Exception as e:
            print(f"Telegram error: {e}")


if __name__ == "__main__":
    print(f"Starting on port {PORT}")
    server = ReuseAddrTCPServer(("", PORT), Handler)
    server.serve_forever()
