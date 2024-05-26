# FastApi
Payment service


## Services

```bash
#inventory service 
fastapi dev main.py --port 80001

#Payment service
fastapi dev main.py --port 80001
```

## Db

```bash
docker run -d --name redis-stack -v /home/pi/data/redismicroservices/:/data -p 6379:6379 -p 8001:8001 -e REDIS_ARGS="--appendonly yes" redis/redis-stack:latest
```
