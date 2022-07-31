import pyotp,base64
from datetime import datetime
from django.conf import settings



class OtpView:

    def get_key(self,phonenumber,email=None):
    	return str(phonenumber)+str(email)+str(datetime.date(datetime.now()))+"FOUSES_CONNECT_KEY"

    def get_otp(self,phonenumber,email=None):
        key=base64.b32encode(self.get_key(phonenumber,email).encode())
        otp=pyotp.TOTP(key,interval=settings.OTP_INTERVAL_TIME)
        return str(otp.now())

    def validate_otp(self,phonenumber,otp,email=None):
    	return self.get_otp(phonenumber,email)==str(otp)

    def send_otp(self,phonenumber,email=None):
    	otp=self.get_otp(phonenumber,email)
    	print(f"Otp for {phonenumber} is",otp)
    	return True