# ===============================================================================#
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#===============================================================================#
### src classes
from src.account import AccountSystem, User, Admin
from src.image import Image
from src.mixin import DictMixin
from src.db.connect import client
from src.db.accountschema import UserSchema
#===============================================================================#

@dataclass
class System(DictMixin):
    account : AccountSystem = field(default_factory=AccountSystem)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', status_code=200)
@app.get('/ping', status_code=200)
@app.post('/ping', status_code=200)
async def healthchk():
    return {'status_code': 200, 'message': 'OK'}


@app.post("/api/register", status_code=201)
async def register_user(user: UserSchema):
    if System.account.register(user) == True:
        return {'status_code': 201, 'message': 'register success'}
    else:
        raise HTTPException(status_code=409, message="E-mail already exists")

@app.post("/api/login", status_code=200)
async def login_user(user: UserSchema):
    System.account.login(user)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
