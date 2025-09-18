import africastalking
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

async def send_sms(customer_phone_number: str, order_message: str):
    """Sends an sms message to a customer"""
    africastalking.initialize(
        username=os.getenv("AFRICAS_TALKING_USERNAME"),
        api_key=os.getenv("AFRICAS_TALKING_API_KEY")
    )
    sms = africastalking.SMS
    try:
        response = sms.send(
            message=order_message,
            recipients=[f"+{customer_phone_number}"]
        )

        print(response)
        if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
            return
        raise HTTPException(
                status_code=400,
                detail="Failed to send SMS"
            )
    except Exception as e:
        raise e
