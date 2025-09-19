from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_sso.sso.google import GoogleSSO
import os
import secrets

from .service import create_customer, customer_login
from .schemas import CustomerCreate, CustomerLogin

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
CALLBACK = "http://localhost:8001/api/v1/auth/google/callback"

# Initialize GoogleSSO
google_sso = GoogleSSO(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, CALLBACK)

customer_router = APIRouter()


@customer_router.post("/register", status_code=201)
async def register_customer(customer: CustomerCreate):
    """API endpoint to handle customer registration"""
    try:
        await create_customer(customer)
        return JSONResponse(status_code=201, content={"message": "Customer registered successfully"})
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while registering user",
        )


@customer_router.post("/login", status_code=200)
async def login_customer(customer: CustomerLogin):
    """API endpoint to handle user login"""
    try:
        login_data = await customer_login(customer)
        return JSONResponse(status_code=200, content=login_data)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while logging in user",
        )


@customer_router.get("/google/login")
async def login_with_google(request: Request):
    """Initiates OAuth2 login with Google"""
    # Generate and store state in session
    state = secrets.token_urlsafe(16)
    request.session["state"] = state

    async with google_sso:
        return await google_sso.get_login_redirect(state=state)


@customer_router.get("/auth/google/callback")
async def google_callback(request: Request):
    """Handles Google OAuth2 callback"""
    try:
        # Extract state values
        state_from_google = request.query_params.get("state")
        state_from_session = request.session.get("state")

        # Debug logging for development
        print("DEBUG: state_from_google =", state_from_google)
        print("DEBUG: state_from_session =", state_from_session)
        print("DEBUG: session contents =", dict(request.session))

        # Validate state (to prevent CSRF attacks)
        if not state_from_session or state_from_google != state_from_session:
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing state parameter"
            )

        # Clear the state from session to prevent replay attacks
        request.session.pop("state", None)

        # Process user info from Google
        async with google_sso:
            user = await google_sso.verify_and_process(request)

        # Ensure response is JSON-serializable
        return JSONResponse(
            content={
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "picture": user.picture,
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=f"Google SSO error: {str(e)}"
        )

    

