import base64
import json
import jwt
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import uuid

# Load private key
with open("privatekey.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# JWT header
header = {
    "alg": "RS384",
    "typ": "JWT"
}

# JWT payload
now = datetime.now(timezone.utc)
payload = {
    "iss": "<Your Client ID>",
    "sub": "<Your Client ID>",
    "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
    "jti": str(uuid.uuid4()),
    "exp": int((now + timedelta(minutes=5)).timestamp()),
    "nbf": int(now.timestamp()),
    "iat": int(now.timestamp())
}

# Encode header and payload
header_json = json.dumps(header)
header_bytes = header_json.encode('utf-8')
encoded_header = base64.urlsafe_b64encode(header_bytes).decode('utf-8').rstrip('=')

payload_json = json.dumps(payload)
payload_bytes = payload_json.encode('utf-8')
encoded_payload = base64.urlsafe_b64encode(payload_bytes).decode('utf-8').rstrip('=')

# Sign the message
message = (encoded_header + '.' + encoded_payload).encode('utf-8')
signature = private_key.sign(
    message,
    padding.PKCS1v15(),
    hashes.SHA384()
)

# Create final JWT
encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
final_jwt = encoded_header + '.' + encoded_payload + '.' + encoded_signature

print(final_jwt)
