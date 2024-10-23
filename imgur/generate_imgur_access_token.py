import requests
from dotenv import load_dotenv
import os
load_dotenv()

url = "https://api.imgur.com/oauth2/token"

refreshToken = os.getenv('IMGUR_REFRESH_TOKEN')
clientId = os.getenv('IMGUR_CLIENT_ID')
clientSecret = os.getenv('IMGUR_CLIENT_SECRET')

payload={'refresh_token': f'{refreshToken}',
'client_id': f'{clientId}',
'client_secret': f'{clientSecret}',
'grant_type': 'refresh_token'}
files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
