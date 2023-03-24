from fastapi import APIRouter, HTTPException

from src.model.account import AccountSystem, Admin, User
from src.schema.accountschema import (
    AccountSchema as AdminSchema, UpdateAccountModel as UpdateAdminModel, 
    UserSchema, UpdateUserModel
)


router = APIRouter()

@router.post('/register', status_code=201)
async def register(user: UserSchema):
    if AccountSystem.register(user):
        return {'status_code': 201, 'detail': 'success'}
    elif AccountSystem.add_user(user.email):
        raise HTTPException(status_code=409, detail='Account already exists')
    else:
        raise HTTPException(status_code=500, detail='Internal Server Error')

@router.post('/login', status_code=200)
async def login(user: UserSchema):
    if AccountSystem.user_login(user):
        return {'status_code': 200, 'detail': 'success'}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')