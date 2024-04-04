import sys,os
sys.path.append(os.path.dirname(sys.path[0]))
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from app.aws.aws_controller import get_items_all

app = FastAPI()

@app.get("/")
async def read_root():
    return  {"response": "hi from server"}

@app.get("/getAllUsers")
async def fetch_users():
    return jsonable_encoder(get_items_all())

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}