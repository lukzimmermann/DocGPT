from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from routers.auth.authService import create_jwt_token, create_new_account, is_valid_user_and_password

router = APIRouter()

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
    message: str
    token: str

class Message(BaseModel):
    message: str

@router.post("/login/", tags=["Auth"])
async def login(data: Credential) -> Token:
    if is_valid_user_and_password(data.email, data.password):
        token = create_jwt_token(data.email)
        return {"message": "login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Wrong username or password")


@router.post("/createAccount/", tags=["Auth"])
async def create_account(data: Credential) -> Message:
    create_new_account(data.email, data.password)
    return {"message": "create account successfully"}

