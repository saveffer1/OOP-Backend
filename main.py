# ===============================================================================#
import os
import glob
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from functools import partial
### docs and admin access config
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
#===============================================================================#
### router
import src.client as endpoint
#===============================================================================#
""" del all resource before start server"""
path = ['server', 'user_avatar', 'server_avatar']
for i in path:
    files = glob.glob(f'resource/{i}/*')
    for f in files:
        os.remove(f)
# ===============================================================================#

def create_app():
    fast_app = FastAPI(title='Discord Clone', docs_url=None, redoc_url=None, openapi_url=None)
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fast_app

app = create_app()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get('/', status_code=200, tags=['healthcheck'])
@app.get('/ping', status_code=200, tags=['healthcheck'])
@app.post('/ping', status_code=200, tags=['healthcheck'])
async def healthchk():
    return {'status_code': 200, 'detail': 'OK'}

@app.get("/admin/doc", tags=['admin'])
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/admin/openapi.json", title="docs")

@app.get("/admin/redoc", tags=['admin'])
async def get_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/admin/openapi.json", title="redoc")

@app.get("/admin/openapi.json", tags=['admin'])
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

app.include_router(endpoint.account_router, prefix='/account', tags=['account'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)

