# Epic FHIR Integration

## What is this?
Backend authentication system for Epic's FHIR R4 API using OAuth2 client credentials flow with RS384-signed JWTs. Implements complete token generation pipeline including RSA key pair creation, manual JWT construction, and authenticated resource fetching.

## Why it exists:
Built to establish secure system-to-system integration with Epic FHIR, one of the largest healthcare API platforms in the US. Enables automated access to patient records, clinical documentation, and other FHIR-compliant resources for healthcare applications.

## How it works:
Authentication Flow:

- Generate RSA-384 public/private key pair
- Register public key with Epic application
- Construct signed JWT with claims (issuer, subject, audience, expiration)
- Exchange JWT for access token via OAuth2 client credentials grant
- Use bearer token to make authenticated FHIR API requests

## Key Components:

- RSA key generation (OpenSSL)
- Manual JWT signing with RS384 algorithm
- Token exchange against Epic's OAuth2 endpoint
- FHIR R4 resource queries with async preferences


## Setup & Usage:

- Python 3.x
- OpenSSL
- Epic FHIR sandbox account with registered application

# Workflow

## Step 1: Generate RSA Key Pair
Generate private key:
openssl genrsa -out privatekey.pem 2048

Generate public key certificate:
openssl req -new -x509 -key privatekey.pem -out publickey509.pem -subj "/CN=myapp"

Upload publickey509.pem to your Epic application's "JWT Signing Public Key" field in the sandbox.
Note: New applications may take 15-30 minutes to synchronize before the client ID is recognized.

## Step 2: Generate Signed JWT

Check generate_jwt.py


## Step 3: Exchange JWT for Access Token
Endpoint: https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token

Request:

POST /interconnect-fhir-oauth/oauth2/token HTTP/1.1

Host: fhir.epic.com

Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&client_assertion=<signed_jwt>

Response:
json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 3600
}

## Step 4: Query FHIR Resources
Endpoint: https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/<resource>
Example - Fetch Document Reference:
http
GET /interconnect-fhir-oauth/api/FHIR/R4/DocumentReference?patient=erXuFYUfucBZaryVksYEcMg3 HTTP/1.1
Host: fhir.epic.com
Accept: application/fhir+json
Prefer: respond-async
Authorization: Bearer <access_token>

Test Patient ID (Sandbox): erXuFYUfucBZaryVksYEcMg3

## Technologies Used:

- Python 3.x
- OpenSSL
- Epic FHIR R4 API
- OAuth2 client credentials flow
- RS384 JWT signing
- Cryptography library

## Resources:

- Epic FHIR Documentation
- FHIR R4 Search Parameters
- Epic Test Patients

## What I Learned:
Healthcare API integration requires understanding cryptographic authentication (RS384 JWT signing), managing short-lived tokens, and navigating extensive technical documentation with limited external support. Debugging authentication flows involves careful attention to timing (token expiration, clock synchronization) and exact specification compliance (claim structure, signature algorithms).
