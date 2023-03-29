# ===============================================================================#
import os
import glob
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from functools import partial
#===============================================================================#
### router
from src.router import (
    router_account, router_document
)
#===============================================================================#
def initial_startup():
    resource = 'resource'
    path = ['server', 'user_avatar', 'server_avatar']
    if os.path.exists(resource):
        """ del all resource before start server"""
        for folder in path:
            files = glob.glob(f'resource/{folder}/*')
            for f in files:
                os.remove(f)
    else:
        """ check if not resource folder create it """
        os.mkdir(resource)
        for folder in path:
            os.mkdir(resource +'/'+ folder)
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

@app.get('/', status_code=200, tags=['healthcheck'])
@app.get('/ping', status_code=200, tags=['healthcheck'])
@app.post('/ping', status_code=200, tags=['healthcheck'])
async def healthchk():
    return {'status_code': 200, 'detail': 'OK'}

app.include_router(router_account, prefix='/account', tags=['account'])
app.include_router(router_document, prefix='/admin', tags=['document'])
