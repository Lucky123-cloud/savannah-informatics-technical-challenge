from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import os

from src.customer.routes import customer_router
from src.order.routes import order_router

app = FastAPI(
        title="Savannah Informatics E-Commerce",
        docs_url="/"
    )

app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv("SECRET_KEY")
    )

app.include_router(customer_router, prefix="/api/v1", tags=["Auth routes"])
app.include_router(order_router, prefix="/api/v1", tags=["Orders routes"])
