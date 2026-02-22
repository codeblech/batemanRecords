import requests
from app.config import config

url = "https://api.imgur.com/oauth2/token"

refreshToken = config.imgur_refresh_token()
clientId = config.imgur_client_id()
clientSecret = config.imgur_client_secret()

payload={'refresh_token': f'{refreshToken}',
'client_id': f'{clientId}',
'client_secret': f'{clientSecret}',
'grant_type': 'refresh_token'}
files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
