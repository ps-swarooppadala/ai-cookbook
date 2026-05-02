import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()  # Needed to run interactive python


async def main():
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

            # List available tools
            tools_result = await session.list_tools()
            print("Available Dynamics 365 CRM tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\n" + "="*50)
            print("Testing Dynamics 365 CRM Tools")
            print("="*50)

            # Test getting accounts
            print("\n1. Getting accounts...")
            try:
                result = await session.call_tool("get_accounts", arguments={
                    "select_fields": "name,accountnumber,telephone1",
                    "top": 5
                })
                print("Accounts result:")
                print(result.content[0].text)
            except Exception as e:
                print(f"Error getting accounts: {e}")

            # Test getting contacts
            print("\n2. Getting contacts...")
            try:
                result = await session.call_tool("get_contacts", arguments={
                    "select_fields": "fullname,emailaddress1,telephone1",
                    "top": 5
                })
                print("Contacts result:")
                print(result.content[0].text)
            except Exception as e:
                print(f"Error getting contacts: {e}")

            # Test getting cases
            print("\n3. Getting cases...")
            try:
                result = await session.call_tool("get_cases", arguments={
                    "select_fields": "title,casenumber,statecode",
                    "top": 5
                })
                print("Cases result:")
                print(result.content[0].text)
            except Exception as e:
                print(f"Error getting cases: {e}")

            # Test getting tasks
            print("\n4. Getting tasks...")
            try:
                result = await session.call_tool("get_tasks", arguments={
                    "select_fields": "subject,statecode,prioritycode",
                    "top": 5
                })
                print("Tasks result:")
                print(result.content[0].text)
            except Exception as e:
                print(f"Error getting tasks: {e}")

            # Test creating an account
            print("\n5. Creating a test account...")
            try:
                result = await session.call_tool("create_account", arguments={
                    "name": "Test Account via MCP",
                    "accountnumber": "ACC-001",
                    "telephone1": "+1-555-0123",
                    "websiteurl": "https://example.com",
                    "description": "Test account created via MCP server"
                })
                print("Create account result:")
                print(result.content[0].text)
            except Exception as e:
                print(f"Error creating account: {e}")

            # Test creating a contact
            print("\n6. Creating a test contact...")
            try:
                result = await session.call_tool("create_contact", arguments={
                    "firstname": "John",
                    "lastname": "Doe",
                    "emailaddress1": "john.doe@example.com",
                    "telephone1": "+1-555-0124",
                    "jobtitle": "Software Engineer"
                })
                print("Create contact result:")
                print(result.content[0].text)
            except Exception as e:
                print(f"Error creating contact: {e}")


if __name__ == "__main__":
    asyncio.run(main())
