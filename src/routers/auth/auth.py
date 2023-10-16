from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from routers.auth.authService import create_jwt_token, create_new_account, is_user_verified, is_valid_user_and_password
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
async def login(data: Credential):

    if not is_user_verified(data.email):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="E-mail is not verified")

    if is_valid_user_and_password(data.email, data.password):
        token = create_jwt_token(data.email)
        token_handler.add_token(data.email, token)
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Wrong username or password")

@router.post("/logout/", tags=["Auth"])
async def logout(data: Token):
    token_handler.delete_token(data.token)
    return {"message": "logout successfully"}

@router.post("/createAccount/", tags=["Auth"])
async def create_account(data: Credential):
    response = create_new_account(data.email, data.password)
    return response

