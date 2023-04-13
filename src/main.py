# ===============================================================================#
import os
import glob
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from functools import partial
from fastapi import Response, Request
#===============================================================================#
### router
from src.router import (
    router_account, router_document
)

ALLOWED_ORIGINS = "http://127.0.0.1:5500"

origins = ['http://127.0.0.1:5500', 'http://localhost:5500', 'http://localhost']

def create_app():
    # middleware = [
    #     Middleware(CORSMiddleware, allow_origins=origins)
    # ]
    fast_app = FastAPI(title='Discord Clone', docs_url=None, redoc_url=None, openapi_url='/admin/openapi.json',)
    
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return fast_app

app = create_app()

@app.on_event("startup")
def initial_startup():
    resource = 'resource'
    path = ['server', 'user_avatar', 'server_avatar']
    if os.path.exists(resource):
        """ del all resource before start server"""
        for folder in path:
            if os.listdir(f'resource/{folder}') != []:
                files = glob.glob(f'resource/{folder}/*')
                for f in files:
                    os.remove(f)
            else:
                continue
    else:
        """ check if not resource folder create it """
        os.mkdir(resource)
        for folder in path:
            os.mkdir(resource + '/' + folder)

@app.get('/', status_code=200, tags=['healthcheck'])
@app.get('/ping', status_code=200, tags=['healthcheck'])
@app.post('/ping', status_code=200, tags=['healthcheck'])
async def healthchk():
    return {'status_code': 200, 'detail': 'OK'}

@app.get('/eiei', status_code=200, tags=['healthcheck'])
async def eiei(resp: Response):
    resp = JSONResponse(status_code=200, content={
                        'status_code': 200, 'detail': 'Authorized'})
    resp.set_cookie(
        "eiei",
        value=f"gg",
        samesite="lax",
        secure=False,
        httponly=True,
        max_age=43200,
    )
    return {'status_code': 200, 'detail': 'OK'}

app.include_router(router_account, prefix='/account')
app.include_router(router_document, prefix='/admin', tags=['document'])


