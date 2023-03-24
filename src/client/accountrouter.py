from fastapi import APIRouter, HTTPException
from src.model.discordsystem import system
from src.schema.accountschema import (
    AccountSchema as AdminSchema, UpdateAccountModel as UpdateAdminModel, 
    UserSchema, UpdateUserModel, LoginSchema
)


router = APIRouter()

@router.post('/register', status_code=201)
async def register(user: UserSchema):
    if system.account.add_user(user):
        return {'status_code': 201, 'detail': 'success', 'data': system.account.user_account}
    else:
        raise HTTPException(status_code=409, detail='Account already exists')

@router.post('/login', status_code=200)
async def login(user: LoginSchema):
    if system.account.user_login(user):
        return {'status_code': 200, 'detail': 'success'}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')    
    