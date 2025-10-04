from fastapi import APIRouter,Response,HTTPException,Body
from app.utils.email import send_email
from app.db.auth import generate_otp
auth_router = APIRouter(prefix="/auth")


@auth_router.post('/send-otp')
async def send_otp_handler(email: str = Body(..., embed=True)):
	otp_obj = generate_otp(email)
 
	send_email(email,otp_obj.otp)
 
	return Response("Otp Sent")
 