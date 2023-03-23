# Discord-OOP-Backend

# How to use

- create config.ini and place into ./src/db

```ini
; config.ini template
[cloudinary]
cloud_name = xxxxxxxxxx
api_key = xxxxxxxxxx
api_secret = xxxxxxxxxx

[mongodb]
user = xxxxxxxxxx
key = xxxxxxxxxx

[JWT]
secret = xxxxxxxxxx
algorithm = HS256
token_expire = 30
```

- run with cmd
  
```cmd
uvicorn main:app --reload
```
