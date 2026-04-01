#!/usr/bin/env python3
"""GHL MCP Server - Multi-location support with PIT tokens."""
import os
import requests
from fastmcp import FastMCP

mcp = FastMCP(name='HighLevel Agency MCP')

GHL_BASE_URL = "https://services.leadconnectorhq.com"

def get_api_key(location_id: str = None):
    if location_id:
        key = os.environ.get(f"GHL_LOCATION_KEY_{location_id}")
        if key:
            return key
    return os.environ.get("GHL_API_KEY")

def ghl_headers(location_id: str = None):
    return {
        "Authorization": f"Bearer {get_api_key(location_id)}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }

# ─── LOCATIONS ───────────────────────────────────────────
@mcp.tool()
def get_locations() -> dict:
    """Get all subaccounts/locations in the agency"""
    r = requests.get(f"{GHL_BASE_URL}/locations/search", headers=ghl_headers())
    return r.json()

# ─── CONTACTS ────────────────────────────────────────────
@mcp.tool()
def get_contacts(location_id: str, query: str = "") -> dict:
    """Get contacts from a specific subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/contacts/", headers=ghl_headers(location_id), params={"locationId": location_id, "query": query})
    return r.json()

@mcp.tool()
def get_contact(location_id: str, contact_id: str) -> dict:
    """Get a single contact by ID"""
    r = requests.get(f"{GHL_BASE_URL}/contacts/{contact_id}", headers=ghl_headers(location_id))
    return r.json()

@mcp.tool()
def create_contact(location_id: str, email: str, firstName: str = "", lastName: str = "", phone: str = "", tags: str = "") -> dict:
    """Create a new contact in HighLevel"""
    payload = {"locationId": location_id, "firstName": firstName, "lastName": lastName, "email": email, "phone": phone}
    if tags:
        payload["tags"] = [t.strip() for t in tags.split(",")]
    r = requests.post(f"{GHL_BASE_URL}/contacts/", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def update_contact(location_id: str, contact_id: str, firstName: str = "", lastName: str = "", email: str = "", phone: str = "", tags: str = "") -> dict:
    """Update an existing contact"""
    payload = {}
    if firstName: payload["firstName"] = firstName
    if lastName:  payload["lastName"] = lastName
    if email:     payload["email"] = email
    if phone:     payload["phone"] = phone
    if tags:      payload["tags"] = [t.strip() for t in tags.split(",")]
    r = requests.put(f"{GHL_BASE_URL}/contacts/{contact_id}", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def add_tags(location_id: str, contact_id: str, tags: str) -> dict:
    """Add tags to a contact (comma-separated tags)"""
    payload = {"tags": [t.strip() for t in tags.split(",")]}
    r = requests.post(f"{GHL_BASE_URL}/contacts/{contact_id}/tags", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def get_tasks(location_id: str, contact_id: str) -> dict:
    """Get all tasks for a contact"""
    r = requests.get(f"{GHL_BASE_URL}/contacts/{contact_id}/tasks", headers=ghl_headers(location_id))
    return r.json()

# ─── CUSTOM FIELDS ───────────────────────────────────────
@mcp.tool()
def get_custom_fields(location_id: str) -> dict:
    """Get all custom fields for a location"""
    r = requests.get(f"{GHL_BASE_URL}/locations/{location_id}/customFields", headers=ghl_headers(location_id))
    return r.json()

@mcp.tool()
def create_custom_field(location_id: str, name: str, dataType: str = "TEXT", placeholder: str = "") -> dict:
    """Create a custom field for a location (dataType: TEXT, LARGE_TEXT, NUMERICAL, PHONE, MONETARY, DATE, CHECKBOX, RADIO, DROPDOWN, MULTISELECT, URL, FILE)"""
    payload = {"name": name, "dataType": dataType, "placeholder": placeholder}
    r = requests.post(f"{GHL_BASE_URL}/locations/{location_id}/customFields", headers=ghl_headers(location_id), json=payload)
    return r.json()

# ─── PIPELINES & OPPORTUNITIES ───────────────────────────
@mcp.tool()
def get_pipelines(location_id: str) -> dict:
    """Get all pipelines in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/opportunities/pipelines", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

@mcp.tool()
def get_opportunities(location_id: str, pipeline_id: str = "", stage_id: str = "") -> dict:
    """List pipeline opportunities with optional pipeline and stage filters"""
    params = {"location_id": location_id}
    if pipeline_id: params["pipelineId"] = pipeline_id
    if stage_id:    params["stageId"] = stage_id
    r = requests.get(f"{GHL_BASE_URL}/opportunities/search", headers=ghl_headers(location_id), params=params)
    return r.json()

@mcp.tool()
def get_opportunity(location_id: str, opportunity_id: str) -> dict:
    """Get a single opportunity by ID"""
    r = requests.get(f"{GHL_BASE_URL}/opportunities/{opportunity_id}", headers=ghl_headers(location_id))
    return r.json()

@mcp.tool()
def create_opportunity(location_id: str, pipeline_id: str, stage_id: str, contact_id: str, name: str, status: str = "open", monetary_value: float = 0) -> dict:
    """Create a new opportunity in a pipeline"""
    payload = {
        "pipelineId": pipeline_id,
        "locationId": location_id,
        "name": name,
        "pipelineStageId": stage_id,
        "status": status,
        "contactId": contact_id,
        "monetaryValue": monetary_value
    }
    r = requests.post(f"{GHL_BASE_URL}/opportunities/", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def update_opportunity(location_id: str, opportunity_id: str, stage_id: str = "", status: str = "", name: str = "", monetary_value: float = 0) -> dict:
    """Update an existing opportunity"""
    payload = {}
    if stage_id:       payload["pipelineStageId"] = stage_id
    if status:         payload["status"] = status
    if name:           payload["name"] = name
    if monetary_value: payload["monetaryValue"] = monetary_value
    r = requests.put(f"{GHL_BASE_URL}/opportunities/{opportunity_id}", headers=ghl_headers(location_id), json=payload)
    return r.json()

# ─── WORKFLOWS ───────────────────────────────────────────
@mcp.tool()
def get_workflows(location_id: str) -> dict:
    """Get all workflows in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/workflows/", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

@mcp.tool()
def get_workflow(location_id: str, workflow_id: str) -> dict:
    """Get a single workflow by ID including name, status, version, triggers and actions"""
    r = requests.get(f"{GHL_BASE_URL}/workflows/{workflow_id}", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

# ─── FUNNELS ─────────────────────────────────────────────
@mcp.tool()
def get_funnels(location_id: str) -> dict:
    """Get all funnels in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/funnels/funnel/list", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

@mcp.tool()
def get_funnel_pages(location_id: str, funnel_id: str) -> dict:
    """Get all pages in a funnel"""
    r = requests.get(f"{GHL_BASE_URL}/funnels/page", headers=ghl_headers(location_id), params={"locationId": location_id, "funnelId": funnel_id})
    return r.json()

@mcp.tool()
def create_funnel_page(location_id: str, funnel_id: str, name: str, html: str) -> dict:
    """Create or update a funnel page with custom HTML in HighLevel"""
    payload = {"name": name, "html": html, "funnelId": funnel_id}
    r = requests.post(f"{GHL_BASE_URL}/funnels/page", headers=ghl_headers(location_id), json=payload)
    return r.json()

# ─── CALENDARS ───────────────────────────────────────────
@mcp.tool()
def get_calendars(location_id: str) -> dict:
    """Get all calendars in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/calendars/", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

@mcp.tool()
def get_calendar_events(location_id: str, calendar_id: str, start_time: str = "", end_time: str = "") -> dict:
    """Get calendar events. start_time and end_time in ISO format e.g. 2026-01-01T00:00:00Z"""
    params = {"locationId": location_id, "calendarId": calendar_id}
    if start_time: params["startTime"] = start_time
    if end_time:   params["endTime"] = end_time
    r = requests.get(f"{GHL_BASE_URL}/calendars/events", headers=ghl_headers(location_id), params=params)
    return r.json()

# ─── CONVERSATIONS & MESSAGES ────────────────────────────
@mcp.tool()
def get_conversations(location_id: str, contact_id: str = "") -> dict:
    """Get conversations in a subaccount, optionally filtered by contact"""
    params = {"locationId": location_id}
    if contact_id: params["contactId"] = contact_id
    r = requests.get(f"{GHL_BASE_URL}/conversations/search", headers=ghl_headers(location_id), params=params)
    return r.json()

@mcp.tool()
def get_messages(location_id: str, conversation_id: str) -> dict:
    """Get all messages in a conversation"""
    r = requests.get(f"{GHL_BASE_URL}/conversations/{conversation_id}/messages", headers=ghl_headers(location_id))
    return r.json()

@mcp.tool()
def send_message(location_id: str, contactId: str, message: str, type: str = "SMS") -> dict:
    """Send a message to a contact (type: SMS, Email, WhatsApp)"""
    payload = {"type": type, "message": message, "contactId": contactId}
    r = requests.post(f"{GHL_BASE_URL}/conversations/messages", headers=ghl_headers(location_id), json=payload)
    return r.json()

# ─── EMAIL TEMPLATES ─────────────────────────────────────
@mcp.tool()
def get_email_templates(location_id: str) -> dict:
    """Get all email templates for a location"""
    r = requests.get(f"{GHL_BASE_URL}/templates/", headers=ghl_headers(location_id), params={"locationId": location_id, "type": "email"})
    return r.json()

@mcp.tool()
def create_email_template(location_id: str, name: str, subject: str, html: str) -> dict:
    """Create a new email template"""
    payload = {"locationId": location_id, "name": name, "subject": subject, "body": html, "type": "email"}
    r = requests.post(f"{GHL_BASE_URL}/templates/", headers=ghl_headers(location_id), json=payload)
    return r.json()

# ─── FORMS ───────────────────────────────────────────────
@mcp.tool()
def get_forms(location_id: str) -> dict:
    """Get all forms in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/forms/", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

# ─── INVOICES ────────────────────────────────────────────
@mcp.tool()
def get_invoices(location_id: str) -> dict:
    """Get all invoices for a location"""
    r = requests.get(f"{GHL_BASE_URL}/invoices/", headers=ghl_headers(location_id), params={"altId": location_id, "altType": "location"})
    return r.json()

# ─── SOCIAL PLANNER ──────────────────────────────────────
@mcp.tool()
def get_social_media_accounts(location_id: str) -> dict:
    """Get all connected social media accounts for a location"""
    r = requests.get(f"{GHL_BASE_URL}/social-media-posting/{location_id}/accounts", headers=ghl_headers(location_id))
    return r.json()

@mcp.tool()
def create_social_post(location_id: str, account_ids: str, content: str, post_date: str = "") -> dict:
    """Create a social media post (account_ids comma-separated, post_date ISO format or empty for immediate)"""
    payload = {
        "locationId": location_id,
        "accountIds": [a.strip() for a in account_ids.split(",")],
        "post": content
    }
    if post_date: payload["scheduleDate"] = post_date
    r = requests.post(f"{GHL_BASE_URL}/social-media-posting/{location_id}/posts", headers=ghl_headers(location_id), json=payload)
    return r.json()

# ─── TAGS ────────────────────────────────────────────────
@mcp.tool()
def get_tags(location_id: str) -> dict:
    """Get all tags for a location"""
    r = requests.get(f"{GHL_BASE_URL}/locations/{location_id}/tags", headers=ghl_headers(location_id))
    return r.json()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port, path="/sse")
