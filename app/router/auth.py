from fastapi import APIRouter,Response,HTTPException,Body, Request, status
from datetime import timedelta
from app.utils.email import send_email
from app.db.auth import generate_otp, verify_user, create_user, create_token, find_user
from app.schemas.auth import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post('/send-otp')
async def send_otp_handler(email: str = Body(..., embed=True)):
    try:
        otp_obj = generate_otp(email)
        send_email(email,otp_obj.otp)
        return Response("Otp Sent")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

 
@auth_router.post('/signup')
async def signup(request: User):

    if not request.email or not request.otp or not request.username:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Verify OTP
    if not verify_user(request.email, request.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    existing_user = find_user(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    existing_username = find_user(request.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    user_data = request.model_dump(exclude={"otp"})
    try:
        new_user = create_user(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )        
        
    token_data = {"sub": new_user.username, "user_id": new_user.id}
    access_token = create_token(
        data=token_data,
        expires_delta=timedelta(minutes=30)
    )

    return {
            "status":"successs",
            "user_id":new_user.id,
            "access_token":access_token
        }
    

    
    
    
