# ===============================================================================#
import os
import glob
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from functools import partial
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
    fast_app = FastAPI(title='Discord Clone')
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fast_app

app = create_app()

@app.get('/', status_code=200)
@app.get('/ping', status_code=200)
@app.post('/ping', status_code=200)
async def healthchk():
    return {'status_code': 200, 'detail': 'OK'}

app.include_router(endpoint.account_router, prefix='/account', tags=['account'])

""" use for test not for cloud upload
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
"""
