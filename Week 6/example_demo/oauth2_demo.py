from oauthlib.oauth2 import WebApplicationClient
import requests

# Cấu hình cho clien của OAuth 2.0 
client_id = 'your-client-id'
client_secret = 'your-client-secret'
redirect_uri = 'http://localhost:5000/callback'
authorization_base_url = 'https://example.com/oauth2/authorize'
token_url = 'https://example.com/oauth2/token'

client = WebApplicationClient(client_id)

# Step 1: Ủy quyền cho URL
authorization_url = client.prepare_request_uri(
    authorization_base_url,
    redirect_uri=redirect_uri,
    scope=['read', 'write']
)
print("Authorization URL:", authorization_url)

# Step 2: Xử lí callback và lấy mã ủy quyền
code = 'sample-authorization-code'  # This would come from the redirect
token_response = client.prepare_token_request(
    token_url,
    authorization_response='code=' + code,
    redirect_url=redirect_uri,
    client_secret=client_secret
)
response = requests.post(token_url, data=token_response)
tokens = client.parse_request_body_response(response.text)
print("Access Token:", tokens['access_token'])