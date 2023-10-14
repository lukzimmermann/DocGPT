from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status
import postgres
import bcrypt
import jwt
import os

load_dotenv()

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

def create_jwt_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(seconds=30)
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm='HS256')

def verify_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms="HS256")
        expire_time = payload.get('exp')
        print(datetime.fromtimestamp(expire_time))
        print(datetime.utcnow())
        if expire_time > datetime.utcnow().timestamp():
            return payload.get('email')
        else:
            raise

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No valid access token")