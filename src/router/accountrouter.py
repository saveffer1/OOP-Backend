import os
import aiofiles
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from src.model.util.email import EmailStr
from src.model.discord_system import system
from src.schema import UserSchema, LoginSchema
from fastapi_login import LoginManager  # Loginmanager Class
from fastapi_login.exceptions import InvalidCredentialsException  # Exception class
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']
manager = LoginManager(SECRET, use_cookie=True, token_url="/login")
manager.cookie_name = "authen"

router = APIRouter()

@manager.user_loader()
def load_user(email: str):
    if email in system.account.user_account:
        return system.account.user_account[email]
    return None

@router.post('/register', status_code=201, tags=['user'])
async def register(account: UserSchema = Depends(UserSchema), image: UploadFile = File(None)):
    
    user = UserSchema(email=account.email, username=account.username, password=account.password)
    if system.account.add_user(user):
        user = system.account.user_account[user.email]
        if image is not None:
            if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
                raise HTTPException(
                    status_code=415, detail='Unsupported Media Type')
            else:
                try:
                    async with aiofiles.open(f'resource/user_avatar/{user.id}_{image.filename}', 'wb') as f:
                        content = await image.read()
                        await f.write(content)
                        # cloudinary_upload(image.filename, public_id=user.id , folder='UserAvatar')
                except:
                    raise HTTPException(
                        status_code=500, detail='Internal Server Error')
                # url = cloudinary_url(f'UserAvatar/{user.id}.{image.content_type}', width=200, height=200, crop="fill")
                # user.avatar = url
                user.avatar = f'resource/user_avatar/{user.id}_{image.filename}'
        return {'status_code': 201, 'detail': 'success', 'data': system.account.user_account}
    else:
        if image is not None:
            # cloudinary_destroy(user.username)
            os.remove(f'resource/user_avatar/{image.filename}')
        del user
        raise HTTPException(status_code=409, detail='Account already exists')

#@manager.user_loader()

@router.post('/login', status_code=200, tags=['user'])
async def login(user: LoginSchema):
    if system.account.user_login(user):
        access_token = manager.create_access_token(data={"sub": user.email})
        resp = RedirectResponse(url="/account/authen", status_code=302)
        manager.set_cookie(resp, access_token)
        return resp
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')    

@router.get('/authen', status_code=200, tags=['user'])
async def getPrivateendpoint(_=Depends(manager)):
    return {'status_code': 200, 'detail': 'success'}