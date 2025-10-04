import random
from .db import session
from datetime import datetime,timedelta
from .models import Otp


def generate_otp(email):
    if not email:
        return None
    otp = str(random.randint(100000, 999999))
    expiry_time = datetime.now() + timedelta(minutes=10)
    
    otp_obj = Otp(
		email = email,
		otp = otp,
		expires_at = expiry_time
	)
    session.add(otp_obj)
    session.commit()
    session.refresh(otp_obj)
    return otp_obj
    