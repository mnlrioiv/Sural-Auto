#!/usr/bin/env python3
"""
Webhook handler for Sural with SO_REUSEADDR.
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
from datetime import datetime
import threading

PORT = 5679
CRM_URL = "https://crm.sural.com.ar/rest/persons"
CRM_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1YjYyZjM0MS03ZWI2LTQ0MTAtODliOC01ZjlkZTkyZGUzNDMiLCJ0eXBlIjoiQVBJX0tFWSIsIndvcmtzcGFjZUlkIjoiNWI2MmYzNDEtN2ViNi00NDEwLTg5YjgtNWY5ZGU5MmRlMzQzIiwiaWF0IjoxNzc0Mjg5OTgwLCJleHAiOjQ5Mjc4ODk5NzksImp0aSI6IjZmYmRhNTk4LWRmZjctNDZiOC04MGIwLWU5Y2Y0YWFiOTExMSJ9.TOvcRyhWNOgiFxB3tZV5K91ryuy2anoD0Z6s82hpQ90"
TELEGRAM_BOT = "8685680710:AAF9SjbV-qFCA_OzympjIdJTHykSoxoNwrU"
TELEGRAM_CHAT = "6728657292"

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
        try:
            req = urllib.request.Request(
                CRM_URL,
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
