from passlib.context import CryptContext
from fastapi import HTTPException

from .repository import CustomerRepository
from .schemas import CustomerCreate, CustomerLogin
from .utils import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
customer_repo = CustomerRepository()

async def create_customer(customer: CustomerCreate) -> None:
    """Handles business logic behind creating a customer"""

    try:
        hashed_password = pwd_context.hash(customer.password)

        customer_repo.create_customer(
                name=customer.name,
                email=customer.email,
                password=hashed_password,
                phone_number=customer.phone_number
            )
        return
    except Exception as e:
        raise e

async def customer_login(customer: CustomerLogin) -> None:
    """Handle business logic behind loging in a customer into their account"""

    try:
        # Query returns a tuple with one element
        user = customer_repo.get_customer_by_email(
                email=customer.email,
            )

        if not user or not pwd_context.verify(customer.password, user["password"]):
            raise HTTPException(
                    status_code=401,
                    detail="Invalid login credentials",
                    headers={"WWW-Authenticate": "Bearer"}
                )

        access_token = create_access_token(data={"sub": user["email"]})
        return {
                "user_id": user["id"],
                "email": user["email"],
                "token_type": "bearer",
                "access_token": access_token
            }
    except Exception as e:
        raise e
