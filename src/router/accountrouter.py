import os
import aiofiles
import bcrypt
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from typing import Optional
from src.model.util.email import EmailStr
from src.model.discord_system import system
from src.schema import UserSchema, LoginSchema

router = APIRouter()

@router.post('/register', status_code=201, tags=['user'])
async def register(account: UserSchema = Depends(UserSchema), image: UploadFile = File(None)):
    hashed_password = bcrypt.hashpw(
        account.password.encode('utf-8'), bcrypt.gensalt(5))
    user = UserSchema(email=account.email, username=account.username,password=hashed_password)
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
    

@router.post('/login', status_code=200, tags=['user'])
async def login(user: LoginSchema):
    if system.account.user_login(user):
        return {'status_code': 200, 'detail': 'success'}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')    
    