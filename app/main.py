from fastapi import FastAPI
from app.routes import auth, users, content

from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
import logging

# Setup logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()

# Konfigurasi rate limiter
limiter = Limiter(key_func=get_remote_address)

# Middleware rate limiting
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Middleware untuk logging setiap request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logging.info(f"{request.method} {request.url} - Status: {response.status_code}")
    return response

# Modul Fitur
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(content.router)