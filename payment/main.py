import time
from typing import Union
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests

app = FastAPI()

redis = get_redis_connection(
    host='192.168.1.88',
    port=6379,
    password=''
)

print("redis->", redis)

@app.get("/")
def read_root():
    return {"Hello": "World"}

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str #pending, completed, refunded
    
    class Meta:
        database = redis
        
@app.get('/orders/{pk}')
def getProduct(pk: str):
    return Order.get(pk)

@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    req = requests.get(f"http://127.0.0.1:8000/products/{body['id']}")
    
    product = req.json()    
    
    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = product['price'] * 0.2,
        total = product['price'] * 1.2,
        quantity = body['quantity'],
        status = 'pending'
    )
    
    order.save()
    
    background_tasks.add_task(OrderCompleted, order)    
    return  order

def OrderCompleted(order: Order):
    time.sleep(5)   
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')



