import hmac
import hashlib
import requests
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization

APP_ID='YOUR_APPLICATION_ID'
APP_INSTALLATION_ID='YOUR_APPLICATION_INSTALLATION_ID'


class Auth(object):
    def __init__(self, private_key):
        self.private_key = private_key

    def get_jwt(self):
        
        due_date = datetime.now() + timedelta(minutes=10) # 10 minutes from now
        expiry = int(due_date.timestamp())
        payload = {
            'iat': int(datetime.now().timestamp() - 60), # 1 minute ago
            'exp': expiry,
            'iss': APP_ID
        }
        priv_rsakey = serialization.load_pem_private_key(self.private_key.encode('utf8'), password=None)

        return jwt.encode(payload, priv_rsakey, algorithm='RS256')

    def get_accesstoken(self):
        token = self.get_jwt()
        resp = requests.post(self.url, headers={'Authorization': f'Bearer {token}'})
        if not resp.ok:
            raise Exception('Failed to get access token')

        return resp.json()['token']


access_token = auth.get_accesstoken()
print(access_token)
# Use the access token to call the GitHub API
