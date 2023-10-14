from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from routers.auth import auth

from routers.auth import auth
from routers.auth.authService import verify_jwt_token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    user = verify_jwt_token(token)
    return {"user": user}
