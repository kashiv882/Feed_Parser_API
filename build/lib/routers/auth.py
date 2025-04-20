from typing import Annotated
import json
import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from jose.utils import base64url_decode
from jose.backends.cryptography_backend import CryptographyRSAKey
from starlette.responses import RedirectResponse

from schemas import UserClaims  # Ensure this path matches your project

route = APIRouter()
security = HTTPBearer()


# Auth0 configuration
AUTH0_DOMAIN = "dev-1w0lpybkl5mp5ht8.us.auth0.com"
API_AUDIENCE = "https://myapiexample.com"
CLIENT_ID = "NCLoOY1Wuh7c70kPNv8SrLoxSHOEseQO"
CLIENT_SECRET = "WVf-ohg-Jbf5Z213SFkzIituGqPqVWMqlBwqvE0carPXsyDY048OlZjsuzBpSWjv"
REDIRECT_URI = "https://feed-parser-api.onrender.com/token"

# Fetch JWKS keys from Auth0
jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
jwks = requests.get(jwks_url).json()["keys"]


def find_public_key(kid: str):
    for key in jwks:
        if key["kid"] == kid:
            return key
    return None


def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    token = credentials.credentials
    try:
        headers = jwt.get_unverified_header(token)
        jwk = find_public_key(headers["kid"])
        if not jwk:
            raise HTTPException(status_code=401, detail="Public key not found")

        rsa_key = CryptographyRSAKey(jwk, algorithm="RS256")


        payload = jwt.decode(
            token,
            rsa_key.to_pem().decode("utf-8"),
            algorithms=["RS256"],
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )

        return UserClaims(
            sub=payload["sub"],
            permissions=payload.get("permissions", []),
            roles=payload.get("https://myapiexample.com/roles", [])
        )

    except (ExpiredSignatureError, JWTError) as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")


@route.get("/login")
def login():
    return RedirectResponse(
        f"https://{AUTH0_DOMAIN}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=offline_access openid profile email"
        f"&audience={API_AUDIENCE}"
        f"&prompt=login"

    )


@route.get("/token")
def get_access_token(code: str):
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        data=payload,
        headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get token")

    return response.json()



















# from typing import Annotated
# import json
# import requests

# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, ExpiredSignatureError, JWTError, JWSError
# from jose.backends.cryptography_backend import RSAAlgorithm
# from starlette.responses import RedirectResponse
# from schemas import UserClaims

# route = APIRouter()
# security = HTTPBearer()

# # Auth0 Configuration
# AUTH0_DOMAIN = "dev-1w0lpybkl5mp5ht8.us.auth0.com"
# API_AUDIENCE = "https://myapiexample.com"
# CLIENT_ID = "NCLoOY1Wuh7c70kPNv8SrLoxSHOEseQO"
# CLIENT_SECRET = "WVf-ohg-Jbf5Z213SFkzIituGqPqVWMqlBwqvE0carPXsyDY048OlZjsuzBpSWjv"
# REDIRECT_URI = "http://localhost:8000/token"

# # Get JWKS (public keys)
# jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
# jwks = requests.get(jwks_url).json()["keys"]

# def find_public_key(kid: str):
#     for key in jwks:
#         if key["kid"] == kid:
#             return key
#     return None

# def validate_token(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
# ):
#     try:
#         token = credentials.credentials
#         unverified_headers = jwt.get_unverified_header(token)

#         jwk = find_public_key(unverified_headers["kid"])
#         if not jwk:
#             raise HTTPException(status_code=401, detail="Public key not found")

#         # Convert JWK to PEM format key
#         public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))

#         # Decode and verify the token
#         token_payload = jwt.decode(
#             token=token,
#             key=public_key,
#             algorithms=["RS256"],
#             audience=API_AUDIENCE,
#             issuer=f"https://{AUTH0_DOMAIN}/",
#         )

#         return UserClaims(
#             sub=token_payload["sub"],
#             permissions=token_payload.get("permissions", []),
#         )

#     except (ExpiredSignatureError, JWTError, JWSError) as error:
#         raise HTTPException(status_code=401, detail=f"Token verification failed: {str(error)}")


# @route.get("/login/")
# def login():
#     return RedirectResponse(
#         f"https://{AUTH0_DOMAIN}/authorize"
#         f"?response_type=code"
#         f"&client_id={CLIENT_ID}"
#         f"&redirect_uri={REDIRECT_URI}"
#         f"&scope=offline_access openid profile email"
#         f"&audience={API_AUDIENCE}"
#         f"&prompt=login"
#     )


# @route.get("/logout")
# def logout():
#     return RedirectResponse(
#         f"https://{AUTH0_DOMAIN}/v2/logout"
#         f"?client_id={CLIENT_ID}"
#         f"&returnTo=http://localhost:8000/login"
#     )


# @route.get("/token")
# def get_access_token(code: str):
#     payload = (
#         f"grant_type=authorization_code"
#         f"&client_id={CLIENT_ID}"
#         f"&client_secret={CLIENT_SECRET}"
#         f"&code={code}"
#         f"&redirect_uri={REDIRECT_URI}"
#     )
#     headers = {"content-type": "application/x-www-form-urlencoded"}

#     response = requests.post(
#         f"https://{AUTH0_DOMAIN}/oauth/token",
#         data=payload,
#         headers=headers
#     )

#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Failed to get token")

#     return response.json()
























# from typing import Annotated
# import requests
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jws, jwt, ExpiredSignatureError, JWTError, JWSError
# from jose.exceptions import JWTClaimsError
# from starlette.responses import RedirectResponse
# from schemas import UserClaims
# # from utils.auth_utils import validate_token

# route = APIRouter()

# security = HTTPBearer()

# jwks_endpoint = "https://dev-1w0lpybkl5mp5ht8.us.auth0.com/.well-known/jwks.json"
# jwks = requests.get(jwks_endpoint).json()["keys"]

# def find_public_key(kid):
#     for key in jwks:
#         if key["kid"] == kid:
#             return key

# def validate_token(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
# ):
#     try:
#         unverified_headers = jws.get_unverified_header(credentials.credentials)
#         token_payload = jwt.decode(
#             token=credentials.credentials,
#             key=find_public_key(unverified_headers["kid"]),
#             audience="https://myapiexample.com",
#             algorithms="RS256",
#         )
#         return UserClaims(
#             sub=token_payload["sub"], permissions=token_payload.get("permissions", [])
#         )
#     except (
#         ExpiredSignatureError,
#         JWTError,
#         JWTClaimsError,
#         JWSError,
#     ) as error:
#         raise HTTPException(status_code=401, detail=str(error))



# @route.get("/login/")
# def login():
#     return RedirectResponse(
#         "https://dev-1w0lpybkl5mp5ht8.us.auth0.com/authorize"
#         "?response_type=code"
#         "&client_id=NCLoOY1Wuh7c70kPNv8SrLoxSHOEseQO"
#         "&redirect_uri=http://localhost:8000/token"
#         "&scope=offline_access openid profile email"
#         "&audience=https://myapiexample.com"
#         "&prompt=login"
#     )


# @route.get("/logout")
# def logout():
#     return RedirectResponse(
#         "https://dev-1w0lpybkl5mp5ht8.us.auth0.com/v2/logout"
#         "?client_id=NCLoOY1Wuh7c70kPNv8SrLoxSHOEseQO"
#         "&returnTo=http://localhost:8000/login"
#     )


# @route.get("/token")
# def get_access_token(code: str):
#     payload = (
#         "grant_type=authorization_code"
#         "&client_id=NCLoOY1Wuh7c70kPNv8SrLoxSHOEseQO"
#         "&client_secret=WVf-ohg-Jbf5Z213SFkzIituGqPqVWMqlBwqvE0carPXsyDY048OlZjsuzBpSWjv"
#         f"&code={code}"
#         f"&redirect_uri=http://localhost:8000/token"
#     )
#     headers = {"content-type": "application/x-www-form-urlencoded"}
#     response = requests.post(
#         "https://dev-1w0lpybkl5mp5ht8.us.auth0.com/oauth/token", payload, headers=headers
#     )
#     return response.json()

