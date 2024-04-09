import sys,os
sys.path.append(os.path.dirname(sys.path[0]))
from typing import Union
from fastapi import FastAPI, Body,Response,Depends,Request
from fastapi.encoders import jsonable_encoder
from app.aws.aws_controller import get_user_by_email,insert_user, update_token ,create_table, get_multi_axes_by_year, insert_energy_analysis_state
from app.model import PostSchema, UserLoginSchema, UserRegisterSchema
from app.auth.auth_handler import signJWT,validate_password,decodeJWT
from app.auth.auth_bearer import JWTBearer
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import EmailStr







app = FastAPI()
users = []

origins = [
   "https://pavanpogula.github.io/",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your list of allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Set the HTTP methods you want to allow
    allow_headers=["*"],  # Set this to your list of allowed headers
)



@app.get("/")
async def read_root():
    return  {"response": "hi from server"}



@app.post("/auth", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(request:Request):
    
    auth_cookie = request.cookies.get("Authorization")
    token = auth_cookie.split("Bearer ")[1]
    data =decodeJWT(token)
    
    return {
        "id":data['user_id']
    }
    



@app.post("/signup", tags=["user"])
def create_user(response: Response,user: UserRegisterSchema = Body(...)):
    data = get_user_by_email(user.email)
    if data['id'] is None:
        return {"message":'500'}
    elif data['id'] == 'none':
        if(insert_user(user)):
            return {"message": "201"}
        else:
            return {"message": "500"}
    return {"message":'409'}
    

@app.post("/user/login", tags=["user"])
def user_login(response: Response,user: UserLoginSchema = Body(...)):
    data = get_user_by_email(user.email)
    if data['id'] is None:
        return {'id':None,"message":'Please Try Again',"code":500}
    elif data['id'] != 'none':
        if validate_password(data['password'],user.password):
            access_token = signJWT(data['id'])
            update_token(data['id'],access_token)
            response.set_cookie(key="Authorization",value=f"Bearer {access_token['access_token']}",httponly=True)
            return {'id':data['id'],"firstname":data['firstname'],"lastname":data['lastname'],"email":data['email'],'message':'Authentication successful','code':200}
    return {'id':None,"code":403,'message':'Invalid credentials'}







@app.get("/checkUser/{email}", tags=["user"])
def user_login(email: EmailStr):
    data = get_user_by_email(email)
    if data['id'] is None:
        return {"message":'500'}
    elif data['id'] == 'none':
       return {'message':'200'}
    return {"message":'409'}

@app.post("/logout", dependencies=[Depends(JWTBearer())], tags=["posts"])
def logout_user(request:Request,response:Response):
    
    auth_cookie = request.cookies.get("Authorization")
    token = auth_cookie.split("Bearer ")[1]
    data =decodeJWT(token)
    access_token={'access_token':''}
    update_token(data['user_id'],access_token)
    response.delete_cookie("Authorization")
    return {
        "message":"success"
    }
 

@app.get("/dashboard/pieData/{state}/{year}",dependencies=[Depends(JWTBearer())],tags=["dashboard"])
async def fetch_dashboard_pie(state:str,year:int):
    return insert_energy_analysis_state(state,year)




@app.get("/dashboard/multiAxesData/{year}",dependencies=[Depends(JWTBearer())],tags=["dashboard"])
async def insert_dashboard_pie(year:int):
    return get_multi_axes_by_year(year)
