from datetime import datetime, timedelta
import os
import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
from src.model.discord_system import system
from src.schema import UserSchema, LoginSchema
from src.model.util import UserStatus, EmailStr, TokenData
from src.router import cloudinary, cloudinary_upload, cloudinary_url, cloudinary_destroy
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

token_manager = TokenData(secret=SECRET, algorithm='HS256')

router = APIRouter()

@router.post('/register', status_code=201, tags=['user'])
async def register(email: EmailStr, username: str, password: str, image: UploadFile = File(None)):
    user = UserSchema(email=email, username=username, password=password)
    if system.account.add_user(user):
        user = system.account.user_account[user.email]
        if image:
            if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
                raise HTTPException(
                    status_code=415, detail='Unsupported Media Type')
            else:
                try:
                    content = await image.read()
                    cloudinary_upload(
                        content,
                        folder="UserAvatar",
                        public_id=f"{user.id}_{user.username}"
                    )
                    url, options = cloudinary_url(f"UserAvatar/{user.id}_{user.username}", width=150, height=150, crop="fill")
                except:
                    raise HTTPException(
                        status_code=500, detail='Internal Server Error')
                user.avatar = url
        else:
            user.avatar = 'https://res.cloudinary.com/dmtnecr2n/image/upload/UserAvatar/DiscordDefaultAvatar.jpg'
        return {'status_code': 201, 'detail': 'success'}
    else:
        del user
        raise HTTPException(status_code=409, detail='Account already exists')


@router.post('/login', status_code=200, tags=['user'])
async def login(user: LoginSchema, request: Request, resp: Response):
    print(user.email, user.password)
    if system.account.user_login(user):
        # if user.email in system.logged_in_users:
        #     system.logged_in_users.remove(user.email)
        #     raise HTTPException(status_code=409, detail='Already logged in on another device or closed the browser without logging out')

        access_token = token_manager.create_access_token(data={"sub": user.email})

        token = jsonable_encoder(access_token)

        resp.set_cookie(
            "authen",
            value=f"{token}",
            samesite="lax",
            secure=False,
            httponly=True,
            max_age=43200,
        )
        
        # system.logged_in_users.add(user.email)
        
        return {'status_code': 200, 'detail': 'Authorized'}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')  

@router.get('/logout', status_code=200, tags=['user'])
async def logout(resp: Response):
    resp.delete_cookie("authen")

@router.get('/auth', status_code=200, tags=['user'])
async def auth(request: Request):
    token = request.cookies.get("authen")
    if token: # check if token exist
        try:
            email = token_manager.decode_access_token(token)
            if email is None: # check if token is valid
                raise HTTPException(status_code=401, detail='Unauthorized 1') 
        except JWTError: # token is not valid
            raise HTTPException(status_code=401, detail='Unauthorized 2') 
        if system.account.user_account[email]: # check if email exist
            return {"status_code": 200, "detail": "Authorized"}
        else: # email not exist
            raise HTTPException(status_code=401, detail='Unauthorized 3') 
    else: # token not exist
        raise HTTPException(status_code=401, detail='Unauthorized 4') 

@router.get('/me', status_code=200, tags=['user'])
async def info(request: Request):
    token = request.cookies.get("authen")
    if token: # check if token exist
        email = token_manager.decode_access_token(token)
        return system.account.user_account[email].get_info()
