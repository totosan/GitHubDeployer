#!/usr/bin/env python3
import jwt
import time
import sys
import requests

# Get PEM file path
if len(sys.argv) > 1:
    pem = sys.argv[1]
else:
    pem = input("Enter path of private PEM file: ")

# Get the App ID
if len(sys.argv) > 2:
    app_id = sys.argv[2]
else:
    app_id = input("Enter your APP ID: ")

# Open PEM
with open(pem, 'rb') as pem_file:
    signing_key = jwt.jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    # GitHub App's identifier
    'iss': app_id
}

# Create JWT
jwt_instance = jwt.JWT()
print(jwt_instance)
encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

resp = requests.post("https://api.github.com/app/installations/37498797/access_tokens", headers={'Authorization': f'Bearer {encoded_jwt}'})
if not resp.ok:
    raise Exception(f'Failed to get access token {resp.content}')

print( resp.json()['token'])