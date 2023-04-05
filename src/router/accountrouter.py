from datetime import datetime, timedelta
import os
import aiofiles
import json
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError
import jwt
from src.model.discord_system import system
from src.schema import UserSchema, LoginSchema
from src.model.util import UserStatus, EmailStr
import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

SECRET = config['cookie']['SECRET_KEY']

router = APIRouter()

@router.post('/register', status_code=201, tags=['user'])
async def register(account: UserSchema = Depends(UserSchema), image: UploadFile | None = None):
    
    user = UserSchema(email=account.email, username=account.username, password=account.password)
    if system.account.add_user(user):
        user = system.account.user_account[user.email]
        if image:
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
        return {'status_code': 201, 'detail': 'success'}
    else:
        if not image:
            # cloudinary_destroy(user.username)
            os.remove(f'resource/user_avatar/{image.filename}')
        del user
        raise HTTPException(status_code=409, detail='Account already exists')   

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm="HS256")
    return encoded_jwt

@router.post('/login', status_code=200, tags=['user'])
async def login(user: LoginSchema):
    if system.account.user_login(user):
        access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(hours=12))

        token = jsonable_encoder(access_token)

        resp = RedirectResponse(url="/account/auth", status_code=302)
        resp.set_cookie(
            "authen",
            value=f"{token}",
            samesite="lax",
            secure=False,
            max_age=3600,
            expires=3600,
        )
        return resp
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')  

@router.get('/logout', status_code=200, tags=['user'])
async def logout(response: Response):
  response = RedirectResponse("/account/login")
  response.delete_cookie(key="authen")
  return response

@router.get('/auth', status_code=200, tags=['user'])
async def auth(request: Request):
    token = request.cookies.get("authen")
    if token:
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            email: EmailStr = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail='Unauthorized 1') 
        except JWTError:
            raise HTTPException(status_code=401, detail='Unauthorized 2') 
        if system.account.user_account[email]:
            return {"status_code": 200, "detail": "Authorized"}
        else:
            raise HTTPException(status_code=401, detail='Unauthorized 3') 
    else:
        raise HTTPException(status_code=401, detail='Unauthorized 4') 

# @router.get('/get_status', status_code=200, tags=['user'])
# async def status(cookie=Depends(manager)):
#     status = system.account.get_status(email=cookie.email)
#     return status

# @router.put('/set_status', status_code=200, tags=['user'])
# async def change_status(status: int, cookie=Depends(manager)):
#     system.account.set_status(email=cookie.email, status=status)

# @router.get('/get_avatar', status_code=200, tags=['user'])
# async def avatar(cookie=Depends(manager)):
#     avatar = system.account.get_avatar(email=cookie.email)
#     return avatar

# @router.put('/set_avatar', status_code=200, tags=['user'])
# async def change_avatar(image: UploadFile = File(None), cookie=Depends(manager)):
#     if image is not None:
#         if image.content_type not in ['image/png', 'image/jpeg', 'image/gif']:
#             raise HTTPException(status_code=415, detail='Unsupported Media Type')
#         else:
#             try:
#                 async with aiofiles.open(f'resource/user_avatar/{cookie.id}_{image.filename}', 'wb') as f:
#                     content = await image.read()
#                     await f.write(content)
#             except:
#                 raise HTTPException(
#                     status_code=500, detail='Internal Server Error')
#             system.account.set_avatar(email=cookie.email, avatar=f'resource/user_avatar/{cookie.id}_{image.filename}')
#         return {'status_code': 200, 'detail': 'success'}
#     else:
#         raise HTTPException(status_code=400, detail='Bad Request')