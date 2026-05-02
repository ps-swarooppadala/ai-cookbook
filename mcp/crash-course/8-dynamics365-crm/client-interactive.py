"""
Interactive Dynamics 365 CRM MCP Client

This client provides an interactive interface to test the D365 CRM MCP server.
You can choose which operations to perform and provide parameters interactively.
"""

import asyncio
import nest_asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()  # Needed to run interactive python


def print_menu():
    """Print the main menu"""
    print("\n" + "="*60)
    print("Dynamics 365 CRM MCP Client - Interactive Mode")
    print("="*60)
    print("GET Operations:")
    print("  1. Get Accounts")
    print("  2. Get Contacts")
    print("  3. Get Cases")
    print("  4. Get Tasks")
    print("\nPOST Operations:")
    print("  5. Create Account")
    print("  6. Create Contact")
    print("  7. Create Case")
    print("  8. Create Task")
    print("\nOther:")
    print("  9. List All Tools")
    print("  0. Exit")
    print("-"*60)


def get_odata_params():
    """Get OData query parameters from user"""
    print("\nOData Query Options (press Enter to skip):")
    select_fields = input("  Select fields (comma-separated): ").strip()
    filter_query = input("  Filter query: ").strip()
    top = input("  Top records (default 10): ").strip()
    
    params = {}
    if select_fields:
        params["select_fields"] = select_fields
    if filter_query:
        params["filter_query"] = filter_query
    if top:
        try:
            params["top"] = int(top)
        except ValueError:
            params["top"] = 10
    else:
        params["top"] = 10
    
    return params


async def handle_get_accounts(session):
    """Handle get accounts operation"""
    print("\n--- Get Accounts ---")
    params = get_odata_params()
    
    try:
        result = await session.call_tool("get_accounts", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_get_contacts(session):
    """Handle get contacts operation"""
    print("\n--- Get Contacts ---")
    params = get_odata_params()
    
    try:
        result = await session.call_tool("get_contacts", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_get_cases(session):
    """Handle get cases operation"""
    print("\n--- Get Cases ---")
    params = get_odata_params()
    
    try:
        result = await session.call_tool("get_cases", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_get_tasks(session):
    """Handle get tasks operation"""
    print("\n--- Get Tasks ---")
    params = get_odata_params()
    
    try:
        result = await session.call_tool("get_tasks", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_create_account(session):
    """Handle create account operation"""
    print("\n--- Create Account ---")
    name = input("Account name (required): ").strip()
    if not name:
        print("Account name is required!")
        return
    
    accountnumber = input("Account number (optional): ").strip()
    telephone1 = input("Primary phone (optional): ").strip()
    websiteurl = input("Website URL (optional): ").strip()
    description = input("Description (optional): ").strip()
    
    params = {"name": name}
    if accountnumber:
        params["accountnumber"] = accountnumber
    if telephone1:
        params["telephone1"] = telephone1
    if websiteurl:
        params["websiteurl"] = websiteurl
    if description:
        params["description"] = description
    
    try:
        result = await session.call_tool("create_account", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_create_contact(session):
    """Handle create contact operation"""
    print("\n--- Create Contact ---")
    firstname = input("First name (required): ").strip()
    lastname = input("Last name (required): ").strip()
    
    if not firstname or not lastname:
        print("First name and last name are required!")
        return
    
    emailaddress1 = input("Email address (optional): ").strip()
    telephone1 = input("Primary phone (optional): ").strip()
    jobtitle = input("Job title (optional): ").strip()
    
    params = {"firstname": firstname, "lastname": lastname}
    if emailaddress1:
        params["emailaddress1"] = emailaddress1
    if telephone1:
        params["telephone1"] = telephone1
    if jobtitle:
        params["jobtitle"] = jobtitle
    
    try:
        result = await session.call_tool("create_contact", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_create_case(session):
    """Handle create case operation"""
    print("\n--- Create Case ---")
    title = input("Case title (required): ").strip()
    if not title:
        print("Case title is required!")
        return
    
    description = input("Description (optional): ").strip()
    customerid = input("Customer ID (optional): ").strip()
    priority = input("Priority (1=High, 2=Normal, 3=Low, default=2): ").strip()
    
    params = {"title": title}
    if description:
        params["description"] = description
    if customerid:
        params["customerid"] = customerid
    if priority:
        try:
            params["prioritycode"] = int(priority)
        except ValueError:
            params["prioritycode"] = 2
    else:
        params["prioritycode"] = 2
    
    try:
        result = await session.call_tool("create_case", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_create_task(session):
    """Handle create task operation"""
    print("\n--- Create Task ---")
    subject = input("Task subject (required): ").strip()
    if not subject:
        print("Task subject is required!")
        return
    
    description = input("Description (optional): ").strip()
    regardingobjectid = input("Related record ID (optional): ").strip()
    priority = input("Priority (0=Low, 1=Normal, 2=High, default=2): ").strip()
    scheduledend = input("Scheduled end (YYYY-MM-DDTHH:MM:SSZ, optional): ").strip()
    
    params = {"subject": subject}
    if description:
        params["description"] = description
    if regardingobjectid:
        params["regardingobjectid"] = regardingobjectid
    if priority:
        try:
            params["prioritycode"] = int(priority)
        except ValueError:
            params["prioritycode"] = 2
    else:
        params["prioritycode"] = 2
    if scheduledend:
        params["scheduledend"] = scheduledend
    
    try:
        result = await session.call_tool("create_task", arguments=params)
        print("\nResult:")
        print(result.content[0].text)
    except Exception as e:
        print(f"Error: {e}")


async def handle_list_tools(session):
    """Handle list tools operation"""
    print("\n--- Available Tools ---")
    try:
        tools_result = await session.list_tools()
        for tool in tools_result.tools:
            print(f"\n🔧 {tool.name}")
            print(f"   Description: {tool.description}")
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                print(f"   Parameters: {tool.inputSchema.get('properties', {}).keys()}")
    except Exception as e:
        print(f"Error: {e}")


async def main():
    """Main interactive loop"""
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server.py"],  # Arguments to the command
    )

    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            
            print("✅ Connected to Dynamics 365 CRM MCP Server")
            
            # Interactive menu loop
            while True:
                print_menu()
                choice = input("Select an option (0-9): ").strip()
                
                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    await handle_get_accounts(session)
                elif choice == "2":
                    await handle_get_contacts(session)
                elif choice == "3":
                    await handle_get_cases(session)
                elif choice == "4":
                    await handle_get_tasks(session)
                elif choice == "5":
                    await handle_create_account(session)
                elif choice == "6":
                    await handle_create_contact(session)
                elif choice == "7":
                    await handle_create_case(session)
                elif choice == "8":
                    await handle_create_task(session)
                elif choice == "9":
                    await handle_list_tools(session)
                else:
                    print("❌ Invalid choice. Please select 0-9.")
                
                if choice != "0":
                    input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
