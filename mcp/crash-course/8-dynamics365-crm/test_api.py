"""
Dynamics 365 API Test Script

This script tests the connection to Dynamics 365 CRM API
to verify your authentication and endpoint configuration.
"""

import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
D365_BASE_URL = "https://orgdaa9efba.crm.dynamics.com"
D365_API_VERSION = "v9.2"
D365_WEB_API_URL = f"{D365_BASE_URL}/api/data/{D365_API_VERSION}"
ACCESS_TOKEN = os.getenv("D365_ACCESS_TOKEN")

async def test_api_connection():
    """Test the Dynamics 365 API connection"""
    print("Dynamics 365 CRM API Connection Test")
    print("=" * 40)
    
    if not ACCESS_TOKEN:
        print("❌ No access token found. Please set D365_ACCESS_TOKEN in your .env file")
        print("   Use auth_helper.py to get an access token")
        return
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # Test endpoints
    endpoints = [
        ("Accounts", "accounts"),
        ("Contacts", "contacts"),
        ("Cases", "incidents"),
        ("Tasks", "tasks")
    ]
    
    async with httpx.AsyncClient() as client:
        for name, endpoint in endpoints:
            print(f"\n🔍 Testing {name} endpoint...")
            url = f"{D365_WEB_API_URL}/{endpoint}?$top=1"
            
            try:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get("value", []))
                    print(f"   ✅ Success - Found {count} record(s)")
                    
                    # Show first record structure if available
                    if count > 0:
                        first_record = data["value"][0]
                        fields = list(first_record.keys())[:5]  # Show first 5 fields
                        print(f"   📋 Available fields (first 5): {', '.join(fields)}")
                else:
                    print(f"   ❌ Error {response.status_code}: {response.text}")
                    
            except httpx.RequestError as e:
                print(f"   ❌ Network error: {e}")
            except Exception as e:
                print(f"   ❌ Unexpected error: {e}")
    
    print("\n🔧 API Information:")
    print(f"   Base URL: {D365_BASE_URL}")
    print(f"   API Version: {D365_API_VERSION}")
    print(f"   Web API URL: {D365_WEB_API_URL}")
    
    print("\n📚 Available OData operations:")
    print("   GET    - Retrieve records")
    print("   POST   - Create records")
    print("   PATCH  - Update records")
    print("   DELETE - Delete records")
    
    print("\n🔍 Common OData query options:")
    print("   $select - Choose specific fields")
    print("   $filter - Filter records")
    print("   $top    - Limit number of records")
    print("   $expand - Include related records")

if __name__ == "__main__":
    asyncio.run(test_api_connection())
