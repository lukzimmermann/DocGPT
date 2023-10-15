from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from routers.auth.authService import create_jwt_token, create_new_account, is_valid_user_and_password
from routers.auth.tokenHandler import TokenHandler

router = APIRouter()

token_handler = TokenHandler()

class Credential(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "hansp44@students.zhaw.ch",
                    "password": "aVerYsTrONgPasSWoRD"
                }
            ]
        }
    }

class Token(BaseModel):
    token: str

class Message(BaseModel):
    message: str

@router.post("/login/", tags=["Auth"])
async def login(data: Credential) -> Token:
    if is_valid_user_and_password(data.email, data.password):
        token = create_jwt_token(data.email)
        token_handler.add_token(data.email, token)
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Wrong username or password")

@router.get("/tokens/", tags=["Auth"])
async def logout():
    print(token_handler.tokens)
    return {"message": "logout successfully"}

@router.post("/logout/", tags=["Auth"])
async def logout(data: Token):
    token_handler.delete_token(data.token)
    return {"message": "logout successfully"}

@router.post("/createAccount/", tags=["Auth"])
async def create_account(data: Credential) -> Message:
    create_new_account(data.email, data.password)
    return {"message": "create account successfully"}

