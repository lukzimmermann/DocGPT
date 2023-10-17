from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from routers.auth import auth

from routers.auth import auth
from routers.auth.authService import verify_jwt_token

description = """
😎
"""

app = FastAPI(title="ZHAW-GPT API", description=description)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth.router)




@app.get("/test/", tags=["Test Endpoint"])
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    user = verify_jwt_token(token)
    return {"user": user}