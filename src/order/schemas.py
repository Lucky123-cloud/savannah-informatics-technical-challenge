from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_id: int
    price: float
    item_id: int
