import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx

load_dotenv("../.env")

# Create an MCP server
mcp = FastMCP(
    name="Dynamics365CRM",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8051,  # only used for SSE transport (set this to any port)
    stateless_http=True,
)

# Dynamics 365 configuration
D365_BASE_URL = "https://orgdaa9efba.crm.dynamics.com"
D365_API_VERSION = "v9.2"
D365_WEB_API_URL = f"{D365_BASE_URL}/api/data/{D365_API_VERSION}"

# OAuth configuration - these should be set in environment variables
CLIENT_ID = os.getenv("D365_CLIENT_ID")
CLIENT_SECRET = os.getenv("D365_CLIENT_SECRET")  # For server-to-server auth
TENANT_ID = os.getenv("D365_TENANT_ID")
ACCESS_TOKEN = os.getenv("D365_ACCESS_TOKEN")  # For testing purposes

class Dynamics365Client:
    def __init__(self):
        self.base_url = D365_WEB_API_URL
        self.access_token = ACCESS_TOKEN
        self.client = httpx.AsyncClient()
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Prefer": "return=representation"
        }
        return headers
    
    async def get_records(self, entity: str, select_fields: Optional[str] = None, 
                         filter_query: Optional[str] = None, top: Optional[int] = None) -> Dict[str, Any]:
        """Get records from Dynamics 365"""
        url = f"{self.base_url}/{entity}"
        
        params = {}
        if select_fields:
            params["$select"] = select_fields
        if filter_query:
            params["$filter"] = filter_query
        if top:
            params["$top"] = top
        
        try:
            response = await self.client.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def create_record(self, entity: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in Dynamics 365"""
        url = f"{self.base_url}/{entity}"
        
        try:
            response = await self.client.post(url, headers=self.get_headers(), json=data)
            response.raise_for_status()
            
            # Get the created record ID from the response headers
            entity_url = response.headers.get("OData-EntityId", "")
            entity_id = entity_url.split("(")[-1].split(")")[0] if entity_url else None
            
            return {
                "success": True,
                "id": entity_id,
                "location": entity_url,
                "data": response.json() if response.content else {}
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def update_record(self, entity: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing record in Dynamics 365"""
        url = f"{self.base_url}/{entity}({record_id})"
        
        try:
            response = await self.client.patch(url, headers=self.get_headers(), json=data)
            response.raise_for_status()
            
            return {
                "success": True,
                "id": record_id,
                "data": response.json() if response.content else {}
            }
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}

# Initialize the D365 client
d365_client = Dynamics365Client()

# Tool for getting accounts
@mcp.tool()
async def get_accounts(select_fields: str = None, filter_query: str = None, top: int = 10) -> str:
    """
    Get account records from Dynamics 365 CRM
    
    Args:
        select_fields: Comma-separated list of fields to select (e.g., "name,accountnumber,telephone1")
        filter_query: OData filter query (e.g., "statecode eq 0")
        top: Maximum number of records to return (default: 10)
    """
    result = await d365_client.get_records("accounts", select_fields, filter_query, top)
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_contacts(select_fields: str = None, filter_query: str = None, top: int = 10) -> str:
    """
    Get contact records from Dynamics 365 CRM
    
    Args:
        select_fields: Comma-separated list of fields to select (e.g., "fullname,emailaddress1,telephone1")
        filter_query: OData filter query (e.g., "statecode eq 0")
        top: Maximum number of records to return (default: 10)
    """
    result = await d365_client.get_records("contacts", select_fields, filter_query, top)
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_cases(select_fields: str = None, filter_query: str = None, top: int = 10) -> str:
    """
    Get case (incident) records from Dynamics 365 CRM
    
    Args:
        select_fields: Comma-separated list of fields to select (e.g., "title,casenumber,statecode")
        filter_query: OData filter query (e.g., "statecode eq 0")
        top: Maximum number of records to return (default: 10)
    """
    result = await d365_client.get_records("incidents", select_fields, filter_query, top)
    return json.dumps(result, indent=2)

@mcp.tool()
async def get_tasks(select_fields: str = None, filter_query: str = None, top: int = 10) -> str:
    """
    Get task records from Dynamics 365 CRM
    
    Args:
        select_fields: Comma-separated list of fields to select (e.g., "subject,statecode,prioritycode")
        filter_query: OData filter query (e.g., "statecode eq 0")
        top: Maximum number of records to return (default: 10)
    """
    result = await d365_client.get_records("tasks", select_fields, filter_query, top)
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_account(name: str, accountnumber: str = None, telephone1: str = None, 
                        websiteurl: str = None, description: str = None) -> str:
    """
    Create a new account in Dynamics 365 CRM
    
    Args:
        name: Account name (required)
        accountnumber: Account number
        telephone1: Primary telephone number
        websiteurl: Website URL
        description: Account description
    """
    data = {"name": name}
    if accountnumber:
        data["accountnumber"] = accountnumber
    if telephone1:
        data["telephone1"] = telephone1
    if websiteurl:
        data["websiteurl"] = websiteurl
    if description:
        data["description"] = description
    
    result = await d365_client.create_record("accounts", data)
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_contact(firstname: str, lastname: str, emailaddress1: str = None, 
                        telephone1: str = None, jobtitle: str = None) -> str:
    """
    Create a new contact in Dynamics 365 CRM
    
    Args:
        firstname: Contact first name (required)
        lastname: Contact last name (required)
        emailaddress1: Primary email address
        telephone1: Primary telephone number
        jobtitle: Job title
    """
    data = {
        "firstname": firstname,
        "lastname": lastname
    }
    if emailaddress1:
        data["emailaddress1"] = emailaddress1
    if telephone1:
        data["telephone1"] = telephone1
    if jobtitle:
        data["jobtitle"] = jobtitle
    
    result = await d365_client.create_record("contacts", data)
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_case(title: str, description: str = None, customerid: str = None, 
                     prioritycode: int = 2) -> str:
    """
    Create a new case (incident) in Dynamics 365 CRM
    
    Args:
        title: Case title (required)
        description: Case description
        customerid: Customer ID (account or contact GUID)
        prioritycode: Priority code (1=High, 2=Normal, 3=Low, default: 2)
    """
    data = {"title": title}
    if description:
        data["description"] = description
    if customerid:
        data["customerid@odata.bind"] = f"/accounts({customerid})"  # Assuming account
    data["prioritycode"] = prioritycode
    
    result = await d365_client.create_record("incidents", data)
    return json.dumps(result, indent=2)

@mcp.tool()
async def create_task(subject: str, description: str = None, regardingobjectid: str = None, 
                     prioritycode: int = 2, scheduledend: str = None) -> str:
    """
    Create a new task in Dynamics 365 CRM
    
    Args:
        subject: Task subject (required)
        description: Task description
        regardingobjectid: Related record ID (account, contact, case, etc.)
        prioritycode: Priority code (0=Low, 1=Normal, 2=High, default: 2)
        scheduledend: Scheduled end date/time (ISO format: YYYY-MM-DDTHH:MM:SSZ)
    """
    data = {"subject": subject}
    if description:
        data["description"] = description
    if regardingobjectid:
        data["regardingobjectid@odata.bind"] = f"/accounts({regardingobjectid})"  # Assuming account
    data["prioritycode"] = prioritycode
    if scheduledend:
        data["scheduledend"] = scheduledend
    
    result = await d365_client.create_record("tasks", data)
    return json.dumps(result, indent=2)

# Run the server
if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running Dynamics 365 CRM MCP server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running Dynamics 365 CRM MCP server with SSE transport")
        mcp.run(transport="sse")
    elif transport == "streamable-http":
        print("Running Dynamics 365 CRM MCP server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown transport: {transport}")
