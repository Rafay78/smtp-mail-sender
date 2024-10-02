from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session
from db import get_db
import schema
from ops import get_or_create_user


auth_router = APIRouter(
    tags=["Google Auth Endpoints"]

)

GOOGLE_CLIENT_ID = "179670820621-h72bmo5vru3eb52equip71kr0kc4kr76.apps.googleusercontent.com"
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
        'openid',
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]


# OAuth2 flow setup
flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
flow.redirect_uri = 'http://localhost:5173'


@auth_router.get("/auth/google")
async def google_auth():
    # Redirect the user to Google's OAuth2 server for consent
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    print(authorization_url)
    return {"authorization_url": authorization_url}



@auth_router.post("/exchange_token")
def exchange_token(req: schema.TokenRequest, db: Session = Depends(get_db)):
    code = req.code
    if code:
        flow.fetch_token(code=code)
        credentials = flow.credentials

        idinfo = id_token.verify_oauth2_token(flow.credentials.id_token, requests.Request(), GOOGLE_CLIENT_ID)


        user_data = {
            "email": idinfo['email'],
            "name": idinfo['name'],
            "picture": HttpUrl(idinfo['picture'])
        }

        user = schema.User(**user_data)

#         # Store or update user in the database here
        user_in_db = get_or_create_user(user, db)

        scopes = credentials.scopes
        print("Granted scopes:", scopes)

        # Now you can use the credentials to interact with Google API or store tokens.
        token_info = {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,            
            "email": idinfo['email'],
            "name": idinfo['name'],
            "picture": HttpUrl(idinfo['picture'])
        }

        return token_info
    else:
        raise HTTPException(detail="No token given", status_code=400)