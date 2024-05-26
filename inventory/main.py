from typing import Union
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


class Product(HashModel):
    name: str
    price:float
    quantity: int
    
    class Meta:
        database = redis
        
        
@app.get('/products')
def all():
    #All primary keys
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
    product = Product.get(pk)
    return {
    "id": product.pk,
    "name": product.name,
    "price":product.price,
    "quantity": product.quantity
    }
    
@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def getProduct(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def productDelete(pk: str):
    return Product.delete(pk)

