import boto3
import hmac
import hashlib
import base64
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config import env_vars
from app.session import session


oauth2_schema = OAuth2PasswordBearer(tokenUrl="signin")
cognito_client = session.client("cognito-idp", region_name=env_vars.REGION)


def calculate_secret_hash(username: str) -> str:
    message = username + env_vars.CLIENT_ID
    dig = hmac.new(
        env_vars.CLIENT_SECRET.encode(), message.encode(), hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()


def create_jwt_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, env_vars.JWT_SECRET, algorithm="HS256")


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, env_vars.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def authenticate_user(token: str = Depends(oauth2_schema)):
    return decode_jwt_token(token)
