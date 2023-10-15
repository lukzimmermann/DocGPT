from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status
from routers.auth.tokenHandler import TokenHandler
import postgres
import bcrypt
import jwt
import os


load_dotenv()

token_handler = TokenHandler()

def is_valid_user_and_password(email: str, password:str) -> bool:
    pg = postgres.PostgresDB()
    pg.connect()

    data = (email,)
    response = pg.selectQuery("""
                   SELECT pass
                   FROM users
                   WHERE email = %s
                   """, data)
    pg.disconnect()

    if response and len(response) == 1:
        stored_hash = response[0][0]
        hash = bcrypt.hashpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

        if hash.decode('utf-8') == stored_hash:
            return True
    
    return False

def create_new_account(email: str, password: str) -> None:
    try:
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)

        pg = postgres.PostgresDB()
        pg.connect()

        data = (email, hashedPassword.decode('utf-8'))

        pg.executeQuery("""
                        INSERT INTO users
                        (email, pass)
                        VALUES (%s, %s)
                        """, data)

        pg.disconnect()
    except:
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal server error")

def create_jwt_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm='HS256')

def verify_jwt_token(token: str) -> str:
    try:
        if not token_handler.is_token_active(token):
            raise
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms="HS256")
        expire_time = payload.get('exp')

        if expire_time > datetime.utcnow().timestamp():
            return payload.get('email')
        else:
            raise

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No valid access token")