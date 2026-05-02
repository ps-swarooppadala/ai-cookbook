"""
Dynamics 365 Authentication Helper

This script helps you get an access token for Dynamics 365 CRM API.
You can use this token in the .env file for testing the MCP server.
"""

import requests
import json
import os
from urllib.parse import urlencode, parse_qs, urlparse

# Configuration
D365_URL = "https://orgdaa9efba.crm.dynamics.com"
CLIENT_ID = "your_client_id_here"  # Replace with your actual client ID
TENANT_ID = "common"  # or your specific tenant ID
REDIRECT_URI = "http://localhost"
RESOURCE = D365_URL

def get_authorization_url():
    """Generate the authorization URL for OAuth flow"""
    auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/authorize"
    
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "resource": RESOURCE,
        "state": "dynamics365_auth"
    }
    
    url = f"{auth_url}?{urlencode(params)}"
    return url

def exchange_code_for_token(authorization_code):
    """Exchange authorization code for access token"""
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
    
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "resource": RESOURCE
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def main():
    print("Dynamics 365 CRM Authentication Helper")
    print("=" * 40)
    
    # Check if CLIENT_ID is configured
    if CLIENT_ID == "your_client_id_here":
        print("❌ Please update the CLIENT_ID in this script with your actual Azure AD application client ID")
        return
    
    print(f"1. Open this URL in your browser:")
    print(get_authorization_url())
    print()
    
    print("2. After authentication, you'll be redirected to localhost.")
    print("   Copy the 'code' parameter from the URL.")
    print()
    
    auth_code = input("3. Enter the authorization code: ").strip()
    
    if not auth_code:
        print("❌ No authorization code provided")
        return
    
    print("\n4. Exchanging code for token...")
    token_response = exchange_code_for_token(auth_code)
    
    if token_response and "access_token" in token_response:
        access_token = token_response["access_token"]
        expires_in = token_response.get("expires_in", "unknown")
        
        print("✅ Success! Access token obtained.")
        print(f"   Expires in: {expires_in} seconds")
        print()
        print("5. Add this token to your .env file:")
        print(f"   D365_ACCESS_TOKEN={access_token}")
        print()
        print("   Or set it as an environment variable:")
        print(f"   export D365_ACCESS_TOKEN='{access_token}'")
        
        # Optionally save to .env file
        env_path = ".env"
        if os.path.exists(env_path):
            save_to_env = input("\n6. Save to .env file? (y/n): ").strip().lower()
            if save_to_env == 'y':
                with open(env_path, 'r') as f:
                    content = f.read()
                
                # Replace or add the token
                lines = content.split('\n')
                token_line = f"D365_ACCESS_TOKEN={access_token}"
                
                # Find and replace existing token line
                found = False
                for i, line in enumerate(lines):
                    if line.startswith("D365_ACCESS_TOKEN="):
                        lines[i] = token_line
                        found = True
                        break
                
                if not found:
                    lines.append(token_line)
                
                with open(env_path, 'w') as f:
                    f.write('\n'.join(lines))
                
                print("✅ Token saved to .env file")
    else:
        print("❌ Failed to obtain access token")

if __name__ == "__main__":
    main()
