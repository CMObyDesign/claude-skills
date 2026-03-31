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

@mcp.tool()
def get_locations() -> dict:
    """Get all subaccounts/locations in the agency"""
    r = requests.get(f"{GHL_BASE_URL}/locations/search", headers=ghl_headers())
    return r.json()

@mcp.tool()
def get_contacts(location_id: str, query: str = "") -> dict:
    """Get contacts from a specific subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/contacts/", headers=ghl_headers(location_id), params={"locationId": location_id, "query": query})
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
def get_pipelines(location_id: str) -> dict:
    """Get all pipelines in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/opportunities/pipelines", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

@mcp.tool()
def get_opportunities(location_id: str) -> dict:
    """List pipeline opportunities"""
    r = requests.get(f"{GHL_BASE_URL}/opportunities/search", headers=ghl_headers(location_id), params={"location_id": location_id})
    return r.json()

@mcp.tool()
def send_message(location_id: str, contactId: str, message: str, type: str = "SMS") -> dict:
    """Send a message to a contact"""
    payload = {"type": type, "message": message, "contactId": contactId}
    r = requests.post(f"{GHL_BASE_URL}/conversations/messages", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def get_workflows(location_id: str) -> dict:
    """Get all workflows in a subaccount"""
    r = requests.get(f"{GHL_BASE_URL}/workflows/", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port, path="/sse")
