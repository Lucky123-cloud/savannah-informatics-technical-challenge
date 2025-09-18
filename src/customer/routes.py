from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_sso.sso.google import GoogleSSO
import os
import hashlib

from .service import create_customer, customer_login
from .schemas import CustomerCreate, CustomerLogin

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
CALLBACK = "https://therabot-backend-fda6ckg8dgbfbfb7.eastus-01.azurewebsites.net/api/v1/auth/google/callback"

google_sso = GoogleSSO(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, CALLBACK)

customer_router = APIRouter()

@customer_router.post("/register", status_code=201)
async def register_customer(customer: CustomerCreate):
    """API endpoint to handle customer registration"""
    try:
        await create_customer(customer)

        return JSONResponse(status_code=201, content="Customer registered successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
        raise HTTPException(
                status_code=500,
                detail="An unexpected error occured while registering user"
            )

@customer_router.post("/login", status_code=200)
async def login_customer(customer: CustomerLogin):
    """API endpoint to handle user login"""
    try:
        login_data = await customer_login(customer)

        return JSONResponse(status_code=200, content=login_data)
    except HTTPException as e:
            raise e
    except Exception as e:
        raise e
        raise HTTPException(
                status_code=500,
                detail="An unexpected error occured while logging in user"
            )

@customer_router.get("/google/login")
async def login_with_google(request: Request):
    """Handles OAuth2 login with Google"""

    # Create state token to prevent CSRF
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session["state"] = state

    async with google_sso:
        return await google_sso.get_login_redirect(state=state)

@customer_router.get("/auth/google/callback")
async def google_callback(request: Request):
    try:
        # Ensure that the request is not a forgery and that the user sending
        # this connect request is the expected user.
        if request.query_params.get("state", "") != request.session["state"]:
            raise HTTPException(
                    status_code=401,
                    detail="Invalid state parameter",
                )
        async with google_sso:
            user = await google_sso.verify_and_process(request)
        return JSONResponse(content=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error logging in user with Google SSO")

