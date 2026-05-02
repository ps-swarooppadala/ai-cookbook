# Dynamics 365 CRM MCP Server

This directory contains an MCP (Model Context Protocol) server and client for interacting with Dynamics 365 CRM REST API endpoints.

## Features

The server provides tools for:

### GET Operations:
- `get_accounts` - Retrieve account records
- `get_contacts` - Retrieve contact records  
- `get_cases` - Retrieve case (incident) records
- `get_tasks` - Retrieve task records

### POST Operations:
- `create_account` - Create new account records
- `create_contact` - Create new contact records
- `create_case` - Create new case records
- `create_task` - Create new task records

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   
   Copy the `.env` file and update with your Dynamics 365 credentials:
   
   ```bash
   # Dynamics 365 CRM Configuration
   D365_CLIENT_ID=your_client_id_here
   D365_CLIENT_SECRET=your_client_secret_here  
   D365_TENANT_ID=your_tenant_id_here
   D365_ACCESS_TOKEN=your_access_token_here
   ```

3. **Get Access Token:**
   
   **Option A: Using the auth helper script (Recommended for testing)**
   ```bash
   python auth_helper.py
   ```
   Follow the prompts to get an access token via OAuth flow.
   
   **Option B: Using Azure CLI**
   ```bash
   az login
   az account get-access-token --resource https://orgdaa9efba.crm.dynamics.com/
   ```
   
   **Option C: Using PowerShell (Azure PowerShell)**
   ```powershell
   Connect-AzAccount
   $token = [Microsoft.Azure.Commands.Common.Authentication.AzureSession]::Instance.AuthenticationFactory.Authenticate($context.Account, $context.Environment, $context.Tenant.Id, $null, "Never", $null, "https://orgdaa9efba.crm.dynamics.com/").AccessToken
   ```

4. **Test API Connection:**
   ```bash
   python test_api.py
   ```
   This will verify your authentication and show available data.

## API Endpoints

The server connects to these Dynamics 365 endpoints:

- **Accounts:** `https://orgdaa9efba.crm.dynamics.com/api/data/v9.2/accounts`
- **Contacts:** `https://orgdaa9efba.crm.dynamics.com/api/data/v9.2/contacts`  
- **Cases:** `https://orgdaa9efba.crm.dynamics.com/api/data/v9.2/incidents`
- **Tasks:** `https://orgdaa9efba.crm.dynamics.com/api/data/v9.2/tasks`

## Running the Server

Start the MCP server:
```bash
python server.py
```

## Running the Client

Run the test client to interact with the server:
```bash
python client-stdio.py
```

## Authentication

The server supports Bearer token authentication. You'll need to:

1. Register an application in Azure Active Directory
2. Grant appropriate permissions to Dynamics 365
3. Obtain an access token using OAuth 2.0 flow
4. Set the token in the `D365_ACCESS_TOKEN` environment variable

## Example Usage

### Getting Records
```python
# Get top 5 accounts with specific fields
result = await session.call_tool("get_accounts", arguments={
    "select_fields": "name,accountnumber,telephone1",
    "top": 5
})

# Get contacts with filter
result = await session.call_tool("get_contacts", arguments={
    "select_fields": "fullname,emailaddress1",
    "filter_query": "statecode eq 0",
    "top": 10
})
```

### Creating Records
```python
# Create a new account
result = await session.call_tool("create_account", arguments={
    "name": "Contoso Ltd",
    "accountnumber": "ACC-001",
    "telephone1": "+1-555-0123",
    "websiteurl": "https://contoso.com"
})

# Create a new contact
result = await session.call_tool("create_contact", arguments={
    "firstname": "John",
    "lastname": "Smith",
    "emailaddress1": "john.smith@contoso.com",
    "jobtitle": "Manager"
})
```

## OData Query Options

The GET tools support OData query parameters:

- **$select:** Choose specific fields to return
- **$filter:** Filter records based on conditions
- **$top:** Limit the number of records returned

Example filters:
- `statecode eq 0` - Active records only
- `createdon gt 2024-01-01T00:00:00Z` - Created after specific date
- `contains(name,'contoso')` - Name contains 'contoso'

## Error Handling

The server includes comprehensive error handling for:
- HTTP errors (authentication, authorization, not found)
- Network connectivity issues
- Invalid request parameters
- Dynamics 365 API errors

All errors are returned as JSON with descriptive error messages.

## Security Notes

- Never commit actual credentials to version control
- Use secure credential storage in production
- Implement proper token refresh logic for long-running applications
- Follow principle of least privilege when configuring Dynamics 365 permissions
