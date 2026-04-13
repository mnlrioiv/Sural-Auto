#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime

DB = "/opt/sural/automation/n8n_data/database.sqlite"
conn = sqlite3.connect(DB)
cur = conn.cursor()


def insert_workflow(name, nodes, connections, description="", trigger_type="webhook"):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    cur.execute("SELECT MAX(CAST(id AS INTEGER)) FROM workflow_entity")
    max_id = cur.fetchone()[0] or 0
    new_id = str(int(max_id) + 1)

    cur.execute("SELECT id FROM project LIMIT 1")
    project_id = cur.fetchone()[0]

    version_id = str(new_id)

    nodes_json = json.dumps(nodes)
    connections_json = json.dumps(connections)
    settings = json.dumps({"executionOrder": "v1"})
    meta = json.dumps({"templateId": "", "templateName": name})

    cur.execute(
        """
        INSERT INTO workflow_entity 
        (id, name, active, nodes, connections, settings, staticData, pinData, versionId, triggerCount, meta, description, isArchived, versionCounter, createdAt, updatedAt)
        VALUES (?, ?, 0, ?, ?, ?, NULL, NULL, ?, 1, ?, ?, 0, 1, ?, ?)
    """,
        (
            new_id,
            name,
            nodes_json,
            connections_json,
            settings,
            version_id,
            meta,
            description,
            now,
            now,
        ),
    )

    cur.execute(
        """
        INSERT INTO shared_workflow (workflowId, projectId, role, createdAt, updatedAt)
        VALUES (?, ?, 'workflow:editor', ?, ?)
    """,
        (new_id, project_id, now, now),
    )

    cur.execute(
        """
        INSERT INTO workflow_published_version (workflowId, publishedVersionId, createdAt)
        VALUES (?, ?, ?)
    """,
        (new_id, version_id, now),
    )

    cur.execute(
        """
        INSERT INTO workflow_history (versionId, workflowId, authors, createdAt, updatedAt, nodes, connections, name, autosaved)
        VALUES (?, ?, '[]', ?, ?, ?, ?, ?, 0)
    """,
        (version_id, new_id, now, now, nodes_json, connections_json, name),
    )

    return new_id


def make_webhook_trigger(path, webhook_id):
    return {
        "id": "webhook-trigger",
        "name": "Webhook Trigger",
        "type": "@n8n/n8n-nodes-base.webhook",
        "typeVersion": 2.2,
        "position": [250, 300],
        "webhookId": webhook_id,
        "parameters": {
            "httpMethod": {"__rl": True, "mode": "list", "value": "POST"},
            "path": path,
            "responseMode": "lastNode",
            "options": {},
        },
    }


def make_http_request(name, method, url, body_fields, pos):
    return {
        "id": f"http-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": pos,
        "parameters": {
            "url": url,
            "method": method,
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "=" + json.dumps(body_fields),
            "options": {"timeout": 30000},
        },
    }


def make_email(name, to, subject, text, pos):
    return {
        "id": f"email-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.emailSend",
        "typeVersion": 1.6,
        "position": pos,
        "parameters": {"to": to, "subject": subject, "text": text, "options": {}},
    }


def make_set(name, assignments, pos):
    return {
        "id": f"set-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": pos,
        "parameters": {
            "mode": "manual",
            "duplicateItem": False,
            "assignments": {"assignments": assignments},
            "options": {},
        },
    }


def make_if(name, conditions, pos):
    return {
        "id": f"if-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.if",
        "typeVersion": 2,
        "position": pos,
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                },
                "conditions": conditions,
                "combinator": "and",
            },
            "options": {},
        },
    }


def make_delay(name, amount, unit, pos):
    return {
        "id": f"delay-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.delay",
        "typeVersion": 2.3,
        "position": pos,
        "parameters": {
            "operation": "timeDelay",
            "amount": amount,
            "unit": unit,
            "options": {},
        },
    }


def make_respond(name, body, pos):
    return {
        "id": f"respond-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.respondToWebhook",
        "typeVersion": 1.4,
        "position": pos,
        "parameters": {
            "respondWith": {"__rl": True, "mode": "json", "value": json.dumps(body)},
            "options": {},
        },
    }


def make_code(name, code, pos):
    return {
        "id": f"code-{name}",
        "name": name,
        "type": "@n8n/n8n-nodes-base.code",
        "typeVersion": 2,
        "position": pos,
        "parameters": {"jsCode": code, "options": {}},
    }


# ==============================================================
# WORKFLOW 1: Lead Reception & Qualification
# ==============================================================
wf1_nodes = [
    make_webhook_trigger("lead-calificacion", "lead-calificacion"),
    make_code(
        "Calificar Lead",
        """
const d = $input.first().json;
const body = d.body || d;

let score = 0;
let tag = "lead_frio";

if (body.email && body.email.includes("@")) score += 20;
if (body.telefono && body.telefono.length > 7) score += 25;
if (body.empresa) score += 15;
if (body.mensaje && body.mensaje.length > 20) score += 20;
if (body.interes === "plataforma completa") { score += 20; tag = "lead_quente"; }
else if (body.interes === "automatizacion") { score += 15; tag = "lead_morno"; }

const empresaTam = body.empleados || "";
if (empresaTam.includes("21") || empresaTam.includes("50")) { score += 15; tag = "lead_quente"; }
if (empresaTam.includes("51")) { score += 20; tag = "lead_quente"; }

return [{json: {...body, lead_score: score, lead_tag: tag, timestamp: new Date().toISOString()}}];
""",
        [550, 300],
    ),
    make_if(
        "Lead quente?",
        [
            {
                "id": "cond-score",
                "leftValue": "={{ $json.lead_score }}",
                "rightValue": "=50",
                "operator": {"type": "string", "operation": "gt"},
            }
        ],
        [850, 300],
    ),
    make_set(
        "Set tag quente",
        [
            {"name": "lead_tag", "value": "lead_quente"},
            {"name": "lead_score", "value": "={{ $json.lead_score }}"},
            {"name": "email", "value": "={{ $json.email }}"},
            {"name": "nombre", "value": "={{ $json.nombre }}"},
            {"name": "empresa", "value": "={{ $json.empresa }}"},
            {"name": "telefono", "value": "={{ $json.telefono }}"},
            {"name": "interes", "value": "={{ $json.interes }}"},
            {"name": "mensaje", "value": "={{ $json.mensaje }}"},
        ],
        [1150, 200],
    ),
    make_set(
        "Set tag frio",
        [
            {"name": "lead_tag", "value": "lead_frio"},
            {"name": "lead_score", "value": "={{ $json.lead_score }}"},
            {"name": "email", "value": "={{ $json.email }}"},
            {"name": "nombre", "value": "={{ $json.nombre }}"},
            {"name": "empresa", "value": "={{ $json.empresa }}"},
            {"name": "telefono", "value": "={{ $json.telefono }}"},
            {"name": "interes", "value": "={{ $json.interes }}"},
            {"name": "mensaje", "value": "={{ $json.mensaje }}"},
        ],
        [1150, 450],
    ),
    make_email(
        "Email bienvenida quente",
        "={{ $json.email }}",
        "Gracias por tu interes, {{ $json.nombre }} - Sural",
        "=Hola {{ $json.nombre }},\n\nGracias por tu interes en Sural. Vimos que te interesa {{ $json.interes }} - es exactamente lo que automatizamos todos los dias.\n\nNuestro equipo se comunicara contigo en las proximas 2 horas para agendar una demo personalizada.\n\nEquipo Sural",
        [1450, 200],
    ),
    make_email(
        "Email bienvenida frio",
        "={{ $json.email }}",
        "Hola {{ $json.nombre }}, tenemos algo para vos - Sural",
        "=Hola {{ $json.nombre }},\n\nGracias por contactingarnos. En Sural ayudamos a empresas como la tuya a automatizar procesos y aumentar ventas.\n\nTe dejamos algunos recursos:\n- Agendas una demo de 15 minutos aqui\n- Ves nuestro video de presentacion\n\nAbrazo,\nEquipo Sural",
        [1450, 450],
    ),
    make_respond(
        "Responder",
        {
            "status": "ok",
            "message": "Lead recibido y calificado",
            "tag": "={{ $json.lead_tag }}",
        },
        [1750, 300],
    ),
]

wf1_connections = {
    "Webhook Trigger": {
        "main": [[{"node": "Calificar Lead", "type": "main", "index": 0}]]
    },
    "Calificar Lead": {
        "main": [[{"node": "Lead quente?", "type": "main", "index": 0}]]
    },
    "Lead quente?": {
        "main": [
            [{"node": "Set tag quente", "type": "main", "index": 0}],
            [{"node": "Set tag frio", "type": "main", "index": 0}],
        ]
    },
    "Set tag quente": {
        "main": [[{"node": "Email bienvenida quente", "type": "main", "index": 0}]]
    },
    "Set tag frio": {
        "main": [[{"node": "Email bienvenida frio", "type": "main", "index": 0}]]
    },
    "Email bienvenida quente": {
        "main": [[{"node": "Responder", "type": "main", "index": 0}]]
    },
    "Email bienvenida frio": {
        "main": [[{"node": "Responder", "type": "main", "index": 0}]]
    },
    "Responder": {"main": [[]]},
}

wf1_id = insert_workflow(
    "Lead Reception & Qualification",
    wf1_nodes,
    wf1_connections,
    "Recibe leads del formulario, los califica por score y envia email de bienvenida segmentado",
)
print(f"Workflow 1 created: id={wf1_id}")

# ==============================================================
# WORKFLOW 2: Follow-up sequences (Schedule-based)
# ==============================================================
wf2_nodes = [
    {
        "id": "scheduled-trigger",
        "name": "Schedule Trigger",
        "type": "@n8n/n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [250, 300],
        "parameters": {"rule": {"interval": [{"field": "cron", "value": "0 9 * * *"}]}},
    },
    make_http_request(
        "Get CRM Leads",
        "GET",
        "http://localhost:3000/api/leads?status=pending",
        {},
        [550, 300],
    ),
    make_code(
        "Filtrar sin seguimiento",
        """
const leads = $input.all();
const now = new Date();
const threeDays = 3 * 24 * 60 * 60 * 1000;

return leads.filter(l => {
    const last = new Date(l.json.updatedAt || l.json.createdAt);
    return (now - last) > threeDays;
}).map(l => l.json);
""",
        [850, 300],
    ),
    make_if(
        "Tiene leads pendientes",
        [
            {
                "id": "has-leads",
                "leftValue": "={{ $json.length }}",
                "rightValue": "=0",
                "operator": {"type": "string", "operation": "gt"},
            }
        ],
        [1150, 300],
    ),
    make_code(
        "Extraer emails",
        """
const leads = $input.all();
return leads.map(l => ({json: {email: l.json.email, nombre: l.json.nombre, empresa: l.json.empresa, id: l.json.id}}));
""",
        [1450, 200],
    ),
    make_email(
        "Follow-up semanal",
        "={{ $json.email }}",
        "Seguimiento: {{ $json.nombre }}, tenemos novedades - Sural",
        "=Hola {{ $json.nombre }},\n\nTe escribimos para saber como vas con la automatizacion en {{ $json.empresa }}.\n\nAlgunas preguntas:\n1. Pudiste ver la demo que te mandamos?\n2. Cual es tu principal dolor operativo hoy?\n3. Te sirve agendar una llamada rapida esta semana?\n\nQuedamos a disposicion,\nEquipo Sural",
        [1750, 200],
    ),
    make_respond(
        "Fin OK",
        {"processed": "={{ $json.email }}", "status": "follow-up sent"},
        [2050, 300],
    ),
    make_respond("Fin Vacio", {"status": "no leads to follow up"}, [1450, 500]),
]

wf2_connections = {
    "Schedule Trigger": {
        "main": [[{"node": "Get CRM Leads", "type": "main", "index": 0}]]
    },
    "Get CRM Leads": {
        "main": [[{"node": "Filtrar sin seguimiento", "type": "main", "index": 0}]]
    },
    "Filtrar sin seguimiento": {
        "main": [[{"node": "Tiene leads pendientes", "type": "main", "index": 0}]]
    },
    "Tiene leads pendientes": {
        "main": [
            [{"node": "Extraer emails", "type": "main", "index": 0}],
            [{"node": "Fin Vacio", "type": "main", "index": 0}],
        ]
    },
    "Extraer emails": {
        "main": [[{"node": "Follow-up semanal", "type": "main", "index": 0}]]
    },
    "Follow-up semanal": {"main": [[{"node": "Fin OK", "type": "main", "index": 0}]]},
    "Fin OK": {"main": [[]]},
    "Fin Vacio": {"main": [[]]},
}

wf2_id = insert_workflow(
    "Weekly Follow-up Sequence",
    wf2_nodes,
    wf2_connections,
    "Ejecuta cada lunes a las 9am. Revisa leads sin seguimiento hace mas de 3 dias y envia follow-up",
)
print(f"Workflow 2 created: id={wf2_id}")

# ==============================================================
# WORKFLOW 3: Budget Generation (via AI Agent)
# ==============================================================
wf3_nodes = [
    make_webhook_trigger("generar-presupuesto", "generar-presupuesto"),
    make_code(
        "Preparar datos presupuesto",
        """
const body = $input.first().json.body || $input.first().json;
return [{json: {
    nombre: body.nombre || "",
    empresa: body.empresa || "",
    tamano: body.empleados || "",
    servicios: body.interes || "",
    presupuesto: body.presupuesto || "",
    email: body.email || "",
    telefono: body.telefono || "",
    timestamp: new Date().toISOString()
}}];
""",
        [550, 300],
    ),
    make_code(
        "Llamar AI Agent",
        """
const d = $input.first().json;
const OpenAI = require('openai');

const client = new OpenAI({apiKey: $env.OPENAI_API_KEY});

const prompt = `Eres el agente de operaciones de Sural. Genera un presupuesto personalizado para:

Cliente: ${d.nombre}
Empresa: ${d.empresa}
Tamano: ${d.tamano}
Servicios requeridos: ${d.servicios}

El presupuesto debe incluir:
1. Plan recomendado (Basic, Pro, Enterprise)
2. Modulos incluidos
3. Precio mensual estimado (ARS)
4. Tiempo de implementacion
5. ROI esperado

Responde en JSON con este formato:
{
  "plan": "...",
  "modulos": [...],
  "precio_mensual": "...",
  "implementacion": "...",
  "roi": "...",
  "notas": "..."
}`;

const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{"role": "user", "content": prompt}],
    response_format: {"type": "json_object"}
});

const content = response.choices[0].message.content;
let presupuesto;
try {
    presupuesto = JSON.parse(content);
} catch(e) {
    presupuesto = {error: "No se pudo generar el presupuesto", raw: content};
}

return [{json: {...d, presupuesto}}];
""",
        [850, 300],
    ),
    make_email(
        "Enviar presupuesto",
        "={{ $json.email }}",
        "Tu presupuesto personalizado - Sural",
        "=Hola {{ $json.nombre }},\n\nGracias por tu interes en Sural. Basandonos en {{ $json.empresa }} ({{ $json.tamano }} empleados), te preparamos el siguiente presupuesto:\n\nPlan: {{ $json.presupuesto.plan }}\nPrecio mensual: {{ $json.presupuesto.precio_mensual }}\n\nModulos incluidos:\n{{ $json.presupuesto.modulos }}\n\nImplementacion: {{ $json.presupuesto.implementacion }}\nROI esperado: {{ $json.presupuesto.roi }}\n\n{{ $json.presupuesto.notas }}\n\nPara avanzar, agenda una llamada aqui: [link calendario]\n\nEquipo Sural",
        [1150, 300],
    ),
    make_respond(
        "Responder presupuesto",
        {
            "status": "ok",
            "message": "Presupuesto generado y enviado",
            "plan": "={{ $json.presupuesto.plan }}",
            "precio": "={{ $json.presupuesto.precio_mensual }}",
        },
        [1450, 300],
    ),
]

wf3_connections = {
    "Webhook Trigger": {
        "main": [[{"node": "Preparar datos presupuesto", "type": "main", "index": 0}]]
    },
    "Preparar datos presupuesto": {
        "main": [[{"node": "Llamar AI Agent", "type": "main", "index": 0}]]
    },
    "Llamar AI Agent": {
        "main": [[{"node": "Enviar presupuesto", "type": "main", "index": 0}]]
    },
    "Enviar presupuesto": {
        "main": [[{"node": "Responder presupuesto", "type": "main", "index": 0}]]
    },
    "Responder presupuesto": {"main": [[]]},
}

wf3_id = insert_workflow(
    "Budget Generation via AI",
    wf3_nodes,
    wf3_connections,
    "Webhook recibe datos del lead y genera un presupuesto personalizado usando OpenAI GPT-4",
)
print(f"Workflow 3 created: id={wf3_id}")

# ==============================================================
# WORKFLOW 4: Support Ticket Automation
# ==============================================================
wf4_nodes = [
    make_webhook_trigger("soporte-ticket", "soporte-ticket"),
    make_code(
        "Clasificar ticket",
        """
const body = $input.first().json.body || $input.first().json;
let priority = "medium";
let category = "general";

const msg = (body.mensaje || body.description || "").toLowerCase();
const subj = (body.asunto || body.subject || "").toLowerCase();

if (msg.includes("urgente") || msg.includes("down") || msg.includes("no funciona")) {
    priority = "high"; category = "technical";
} else if (msg.includes("factura") || msg.includes("pago") || msg.includes("cobro")) {
    priority = "low"; category = "billing";
} else if (msg.includes("como") || msg.includes("help") || msg.includes("ayuda")) {
    priority = "low"; category = "support";
}

return [{json: {...body, ticket_priority: priority, ticket_category: category, createdAt: new Date().toISOString()}}];
""",
        [550, 300],
    ),
    make_if(
        "Es urgente?",
        [
            {
                "id": "cond-urg",
                "leftValue": "={{ $json.ticket_priority }}",
                "rightValue": "=high",
                "operator": {"type": "string", "operation": "equals"},
            }
        ],
        [850, 300],
    ),
    make_email(
        "Respuesta urgente",
        "={{ $json.email }}",
        "[URGENTE] Recibimos tu consulta - Sural",
        "=Hola {{ $json.nombre }},\n\nRecibimos tu mensaje urgente. Nuestro equipo tecnico esta siendo notificado y te responderemos en menos de 1 hora.\n\nNumero de ticket: {{ $json.id }}\n\nEquipo Sural - Soporte",
        [1150, 200],
    ),
    make_email(
        "Respuesta normal",
        "={{ $json.email }}",
        "Recibimos tu consulta - Sural",
        "=Hola {{ $json.nombre }},\n\nGracias por contactingarnos. Tu consulta sera respondida en las proximas 24 horas.\n\nCategoria: {{ $json.ticket_category }}\nPrioridad: {{ $json.ticket_priority }}\n\nEquipo Sural",
        [1150, 450],
    ),
    make_code(
        "Crear ticket CRM",
        """
const d = $input.first().json;
return [{json: {
    action: "create_ticket",
    title: d.asunto || "Soporte de " + d.nombre,
    priority: d.ticket_priority,
    category: d.ticket_category,
    customer_email: d.email,
    customer_name: d.nombre,
    description: d.mensaje || "",
    channel: "web"
}}];
""",
        [1450, 300],
    ),
    make_http_request(
        "POST Ticket to CRM",
        "POST",
        "http://localhost:3000/api/tickets",
        {
            "title": "={{ $json.title }}",
            "priority": "={{ $json.priority }}",
            "customer_email": "={{ $json.customer_email }}",
            "description": "={{ $json.description }}",
            "channel": "={{ $json.channel }}",
        },
        [1750, 300],
    ),
    make_respond(
        "Fin soporte",
        {
            "status": "ok",
            "ticket_created": True,
            "priority": "={{ $json.ticket_priority }}",
        },
        [2050, 300],
    ),
]

wf4_connections = {
    "Webhook Trigger": {
        "main": [[{"node": "Clasificar ticket", "type": "main", "index": 0}]]
    },
    "Clasificar ticket": {
        "main": [[{"node": "Es urgente?", "type": "main", "index": 0}]]
    },
    "Es urgente?": {
        "main": [
            [{"node": "Respuesta urgente", "type": "main", "index": 0}],
            [{"node": "Respuesta normal", "type": "main", "index": 0}],
        ]
    },
    "Respuesta urgente": {
        "main": [[{"node": "Crear ticket CRM", "type": "main", "index": 0}]]
    },
    "Respuesta normal": {
        "main": [[{"node": "Crear ticket CRM", "type": "main", "index": 0}]]
    },
    "Crear ticket CRM": {
        "main": [[{"node": "POST Ticket to CRM", "type": "main", "index": 0}]]
    },
    "POST Ticket to CRM": {
        "main": [[{"node": "Fin soporte", "type": "main", "index": 0}]]
    },
    "Fin soporte": {"main": [[]]},
}

wf4_id = insert_workflow(
    "Support Ticket Automation",
    wf4_nodes,
    wf4_connections,
    "Recibe tickets de soporte desde la web, los clasifica por prioridad y crea casos en CRM",
)
print(f"Workflow 4 created: id={wf4_id}")

# ==============================================================
# WORKFLOW 5: Marketing Nurturing Sequence
# ==============================================================
wf5_nodes = [
    {
        "id": "new-lead-trigger",
        "name": "Webhook New Lead",
        "type": "@n8n/n8n-nodes-base.webhook",
        "typeVersion": 2.2,
        "position": [250, 300],
        "webhookId": "marketing-new-lead",
        "parameters": {
            "httpMethod": {"__rl": True, "mode": "list", "value": "POST"},
            "path": "marketing-new-lead",
            "responseMode": "lastNode",
            "options": {},
        },
    },
    make_set(
        "Guardar lead data",
        [
            {"name": "email", "value": "={{ $json.body.email }}"},
            {"name": "nombre", "value": "={{ $json.body.nombre }}"},
            {"name": "empresa", "value": "={{ $json.body.empresa }}"},
            {"name": "interes", "value": "={{ $json.body.interes }}"},
            {"name": "tag", "value": "={{ $json.lead_tag || 'new_lead' }}"},
        ],
        [550, 300],
    ),
    make_email(
        "Email dia 0 - Bienvenida",
        "={{ $json.email }}",
        "Bienvenido {{ $json.nombre }}, estas a un paso de automatizar tu negocio - Sural",
        "=Hola {{ $json.nombre }},\n\nBienvenido a Sural! Estamos muy contentos de que {{ $json.empresa }} este interesado en automatizar {{ $json.interes }}.\n\nEn los proximos dias te vamos a compartir:\n- Casos de exito de empresas similares\n- Una guia de automatizacion para tu industria\n- Una demo personalizada cuando estes listo\n\nMientras tanto, si queres adelantar, la agenda aqui: [link]\n\nAbrazo,\nMarcos - Fundador de Sural",
        [850, 200],
    ),
    make_delay("Esperar 3 dias", 3, "days", [1150, 200]),
    make_email(
        "Email dia 3 - Educacion",
        "={{ $json.email }}",
        "{{ $json.nombre }}, 3 tips para automatizar tu empresa hoy - Sural",
        "=Hola {{ $json.nombre }},\n\nTe queria compartir 3 automatizaciones que pueden cambiar el juego en {{ $json.empresa }}:\n\n1. **Respuestas automaticas en WhatsApp** - Contesta 24/7 sin estar pegado al telefono\n2. **Captura de leads automatica** - Todo lead que llega de tu web se registra solo en tu CRM\n3. **Seguimiento inteligente** - El sistema les manda mensajes a tus leads que no contestaron\n\nQueres ver como funciona? Agendamos 15 minutos: [link]\n\nMarcos",
        [1450, 200],
    ),
    make_delay("Esperar 7 dias", 7, "days", [1750, 200]),
    make_email(
        "Email dia 10 - Oferta",
        "={{ $json.email }}",
        "{{ $json.nombre }}, oferta especial para {{ $json.empresa }} - Sural",
        "=Hola {{ $json.nombre }},\n\nDesde que te contactaste con nosotros, {{ $json.empresa }} sigue igual? Jaja, bueno, si todavia no automatizaron, tenemos una oferta para vos:\n\n**Implementacion gratuita** para las primeras 5 empresas que se inscriban este mes.\n\nSolo tenes que agendar una llamada de 20 minutos y te mostramos todo. Sin compromiso.\n\n[Agendar ahora]\n\nTe dejo un caso de estudio de una empresa similar a la tuya: [link caso]\n\nMarcos",
        [2050, 200],
    ),
    make_respond(
        "Fin nurturing",
        {"status": "ok", "sequence": "started", "emails_count": 3},
        [2350, 200],
    ),
]

wf5_connections = {
    "Webhook New Lead": {
        "main": [[{"node": "Guardar lead data", "type": "main", "index": 0}]]
    },
    "Guardar lead data": {
        "main": [[{"node": "Email dia 0 - Bienvenida", "type": "main", "index": 0}]]
    },
    "Email dia 0 - Bienvenida": {
        "main": [[{"node": "Esperar 3 dias", "type": "main", "index": 0}]]
    },
    "Esperar 3 dias": {
        "main": [[{"node": "Email dia 3 - Educacion", "type": "main", "index": 0}]]
    },
    "Email dia 3 - Educacion": {
        "main": [[{"node": "Esperar 7 dias", "type": "main", "index": 0}]]
    },
    "Esperar 7 dias": {
        "main": [[{"node": "Email dia 10 - Oferta", "type": "main", "index": 0}]]
    },
    "Email dia 10 - Oferta": {
        "main": [[{"node": "Fin nurturing", "type": "main", "index": 0}]]
    },
    "Fin nurturing": {"main": [[]]},
}

wf5_id = insert_workflow(
    "Marketing Nurturing Sequence",
    wf5_nodes,
    wf5_connections,
    "Nurturing automatizado: email de bienvenida + educacion a los 3 dias + oferta a los 7 dias",
)
print(f"Workflow 5 created: id={wf5_id}")

conn.commit()
conn.close()
print("\nAll workflows created successfully!")
