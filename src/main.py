from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv  #Import dotenv

# Load environment variables from .env
load_dotenv()

from src.customer.routes import customer_router
from src.order.routes import order_router

app = FastAPI(
    title="Savannah Informatics Online Store",
    docs_url="/"
)

# Ensure SECRET_KEY is loaded from .env
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "fallbacksecret")  # fallback to avoid crash
)

# Routers
app.include_router(customer_router, prefix="/api/v1", tags=["Auth routes"])
app.include_router(order_router, prefix="/api/v1", tags=["Orders routes"])
