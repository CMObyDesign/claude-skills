#!/usr/bin/env python3
"""GHL MCP Server - Multi-location support with PIT tokens."""
import os
import requests
import uvicorn
from fastmcp import FastMCP

mcp = FastMCP(name='HighLevel Agency MCP')

GHL_BASE_URL = "https://services.leadconnectorhq.com"

def get_api_key(location_id=None):
    if location_id:
        key = os.environ.get(f"GHL_LOCATION_KEY_{location_id}")
        if key:
            return key
    return os.environ.get("GHL_API_KEY")

def ghl_headers(location_id=None):
    return {
        "Authorization": f"Bearer {get_api_key(location_id)}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }

@mcp.tool()
def get_locations(input: dict) -> dict:
    """Get all subaccounts/locations in the agency"""
    r = requests.get(f"{GHL_BASE_URL}/locations/search", headers=ghl_headers())
    return r.json()

@mcp.tool()
def get_contacts(input: dict) -> dict:
    """Search and list contacts in HighLevel"""
    location_id = input.get("location_id")
    params = {"locationId": location_id, "query": input.get("query", "")}
    r = requests.get(f"{GHL_BASE_URL}/contacts/", headers=ghl_headers(location_id), params=params)
    return r.json()

@mcp.tool()
def create_contact(input: dict) -> dict:
    """Create a new contact in HighLevel"""
    location_id = input.get("location_id")
    payload = {
        "locationId": location_id,
        "firstName": input.get("firstName", ""),
        "lastName": input.get("lastName", ""),
        "email": input.get("email", ""),
        "phone": input.get("phone", ""),
        "tags": input.get("tags", [])
    }
    r = requests.post(f"{GHL_BASE_URL}/contacts/", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def get_pipelines(input: dict) -> dict:
    """Get all pipelines in HighLevel"""
    location_id = input.get("location_id")
    r = requests.get(f"{GHL_BASE_URL}/opportunities/pipelines", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

@mcp.tool()
def get_opportunities(input: dict) -> dict:
    """List pipeline opportunities"""
    location_id = input.get("location_id")
    r = requests.get(f"{GHL_BASE_URL}/opportunities/search", headers=ghl_headers(location_id), params={"location_id": location_id})
    return r.json()

@mcp.tool()
def send_message(input: dict) -> dict:
    """Send a message to a contact"""
    location_id = input.get("location_id")
    payload = {
        "type": input.get("type", "SMS"),
        "message": input.get("message", ""),
        "contactId": input.get("contactId")
    }
    r = requests.post(f"{GHL_BASE_URL}/conversations/messages", headers=ghl_headers(location_id), json=payload)
    return r.json()

@mcp.tool()
def get_workflows(input: dict) -> dict:
    """Get all workflows in HighLevel"""
    location_id = input.get("location_id")
    r = requests.get(f"{GHL_BASE_URL}/workflows/", headers=ghl_headers(location_id), params={"locationId": location_id})
    return r.json()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        mcp.http_app(path="/sse"),
        host="0.0.0.0",
        port=port
    )
