# # import sys
# # print(sys.path)
# from fastapi import FastAPI, Depends, HTTPException
# from jose import jwt, JWTError
# from datetime import datetime, timedelta

# from jose import jwt, JWTError
# from datetime import datetime, timedelta
# #from fastapi.security import OAuth2PasswordRequestForm
# from fastapi.security import OAuth2PasswordRequestForm
# #from typing import Annotated
# from typing import Annotated


# ALGORITHM = "HS256"
# SECRET_KEY = "Secure Secret Key"

# def create_access_token(subject: str , expires_delta: timedelta) -> str:
#     expire = datetime.utcnow() + expires_delta
#     to_encode = {"exp": expire, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# app = FastAPI()

# fake_users_db: dict[str, dict[str, str]] = {
#     "ameenalam": {
#         "username": "ameenalam",
#         "full_name": "Ameen Alam",
#         "email": "ameenalam@example.com",
#         "password": "secret",
#     },
#     "mjunaid": {
#         "username": "mjunaid",
#         "full_name": "Muhammad Junaid",
#         "email": "mjunaid@example.com",
#         "password": "secret",
#     },
# }

# @app.post("/login")
# def login_request(data_from_user: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
#     #return {"username": data_from_user.username, "password": data_from_user.password }

#     #step 1 username exit in database - Else error
#     user_in_fake_db = fake_users_db.get(data_from_user.username)
#     if user_in_fake_db is None:
#         raise HTTPException(status_code=400, detail="Incorrect username")
#     #step2 check password  - Else Error
#     if user_in_fake_db["password"] != data_from_user.password:
#         raise HTTPException(status_code=400, detail="Incorrect password")
#     #step3 Generate token

#     access_token_expiry_minutes = timedelta(minutes=1)
#     generated_token = create_access_token(
#         subject= data_from_user.username, expires_delta=access_token_expiry_minutes
#     )
#     return {"username": data_from_user.username, "access_token":generated_token}

#     #return {"username": data_from_user.username, "password": data_from_user.password }

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
# @app.get("/get-token")
# def get_token(name: str):

#     access_token_expiry_minutes = timedelta(minutes=1)
#     print("access_token_expirty_minutes", access_token_expiry_minutes)

#     generated_token = create_access_token(subject=name, expires_delta=access_token_expiry_minutes)
#     return {"access_token": generated_token}

# def decode_access_token(token: str):
#     decoded_data = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
#     return decoded_data

# @app.get("/decode-token")
# def decode_token(token: str):
#     try:
#         decoded_data = decode_access_token(token)
#         return decoded_data
   
         
#     except JWTError as e:
#         return {"error": str(e)}
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}




from fastapi import FastAPI, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
#from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

ALGORITHM = "HS256"
SECRET_KEY = "Secure Secret Key"

def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()
# Multiple Microservice - 1 Auth Microservice
#Step 1: Wrapper Endpoint That takes formata and call auth service login endpoint
#Step 2:  import oAuth2password Bearer - token URl - wrapper Endpoint API path
#step 3: oaut2_scheme = pass to All Endpoints in Dependcy
oauth_scheme = OAuth2PasswordBearer(tokenUrl= "login-endpoint")

fake_users_db: dict[str, dict[str, str]] = {
    "ameenalam": {
        "username": "ameenalam",
        "full_name": "Ameen Alam",
        "email": "ameenalam@example.com",
        "password": "secret",
    },
    "mjunaid": {
        "username": "mjunaid",
        "full_name": "Muhammad Junaid",
        "email": "mjunaid@example.com",
        "password": "secret",
    },
    "saqlain":{
        "username": "saqlain",
        "full_name": "zahoor",
        "email":"engsaqlainzahoor@gmail.com",
        "password":"admin"
    }
}

@app.post("/login-endpoint")
def login_request(data_from_user: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    user_in_fake_db = fake_users_db.get(data_from_user.username)
    if user_in_fake_db is None:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    if user_in_fake_db["password"] != data_from_user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token_expiry_minutes = timedelta(minutes=1)
    generated_token = create_access_token(
        subject=data_from_user.username, expires_delta=access_token_expiry_minutes
    )
    return {"username": data_from_user.username, "access_token": generated_token}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/all-users")
def get_all_users(token:Annotated[str, Depends(oauth_scheme)]):
#def get_all_users():
    return fake_users_db

@app.get("/special-items")
def get_special_items(token: Annotated[str, Depends(oauth_scheme)]):
    #Decode Token
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
    return{"special":"items", "decoded_data": decoded_data}

@app.get("/get-token")
def get_token(name: str):
    access_token_expiry_minutes = timedelta(minutes=1)
    generated_token = create_access_token(subject=name, expires_delta=access_token_expiry_minutes)
    return {"access_token": generated_token}

def decode_access_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/decode-token")
def decode_token(token: str):
    try:
        decoded_data = decode_access_token(token)
        return decoded_data
    except HTTPException as e:
        return {"error": e.detail}
    except Exception as e:
        return {"error": str(e)}
