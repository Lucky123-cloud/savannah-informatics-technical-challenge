from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .service import create_new_order, get_order, remove_order
from .schemas import OrderCreate

order_router = APIRouter()

@order_router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    """API endpoint to create a new order in the database"""

    try:
        await create_new_order(order)

        return JSONResponse(status_code=201, content={"message": "Order created successfully"})
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
                status_code=500,
                detail="An unexpected error occured"
            )

@order_router.get("/orders/{order_id}")
async def retrieve_order(order_id: int):
    """API endpoint to retrieve an order"""
    try:
        order = await get_order(order_id)

        return JSONResponse(status_code=200, content=order)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
        raise HTTPException(
                status_code=500,
                detail="An unexpected error occured"
            )

@order_router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    """API endpoint to delete an order from the database"""
    try:
        await remove_order(order_id)

        return JSONResponse(status_code=200, content={"message": "Order deleted successfully"})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
        raise HTTPException(
                status_code=500,
                detail="An unexpected error occured"
            )
