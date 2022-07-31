from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth import authenticate


from .serializers import *
from .permissions import *
from .otp import OtpView


from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenObtainPairView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):

	def post(self,request):
		data=request.data
		phonenumber=data.get("phonenumber")
		password=data.get("password")
		if not phonenumber: return Response({"message":"phonenumber field missing !"},400)
		if not password: return Response({"message":"password field missing !"},400)
		check=authenticate(request,phonenumber=phonenumber,password=password)
		if check is not None:
			refresh=RefreshToken.for_user(check)
			data={
				  "message":"success",
				  "refresh_token":str(refresh),
				  "access_token":str(refresh.access_token),
				  "data":UserSerializer(check).data
				 }
			return Response(data,200)
		else:
			return Response({"message":"Invalid phonenumber or password"},400)


class SignupView(APIView):

	def post(self,request):
		data=request.data
		password=request.data.get("password")
		phonenumber=request.data.get("phonenumber")
		if not password: return Response({"message":"password is required"},400)
		serializer=UserSerializer(data=data)
		if(serializer.is_valid()):
			try:
				OtpView().send_otp(phonenumber)
			except Exception as err:
				return Response({"message":str(err)},400)
		else:
			return Response({"message":list(serializer.errors.values())[0][0]},400)
		return Response({"message":"Otp Sent Successfully"},200)

	def put(self,request):
		data=request.data
		password=request.data.get("password")
		otp=request.data.get("otp")
		phonenumber=request.data.get("phonenumber")
		if not password: return Response({"message":"password is required"},400)
		if not otp: return Response({"message":"otp is required"},400)
		serializer=UserSerializer(data=data)
		if(serializer.is_valid()):
			try:
				temp=OtpView().validate_otp(phonenumber,otp)
				if not temp:
					return Response({"message":"Invalid Otp"},400)
			except Exception as err:
				return Response({"message":str(err)},400)
			obj=serializer.save()
			obj.set_password(password)
			obj.active=True
			obj.save()
		else:
			return Response({"message":list(serializer.errors.values())[0][0]},400)
		return Response({"message":"Account Created Successfully"},200)



class OtpVerifyView(APIView):

	def get(self,request):
		phonenumber=request.GET.get('phonenumber')
		if not phonenumber: return Response({"message":"please provide valid phonenumber"},400)
		try:
			OtpView().send_otp(phonenumber)
		except Exception as err:
			return Response({"message":str(err)},400)
		return Response({"message":"Otp sent Successfully"},200)

	def post(self,request):
		phonenumber=request.data.get("phonenumber")
		otp=request.data.get("otp")
		if not phonenumber: return Response({"message":"please provide valid phonenumber"},400)
		if not otp: return Response({"message":"please provide valid otp"},400)
		try:
			temp=OtpView().validate_otp(phonenumber,otp)
			if not temp:
				return Response({"message":"Invalid Otp"},400)
		except Exception as err:
			return Response({"message":str(err)},400)
		return Response({"message":"otp verified successfully"},200)




class ForgotPasswordView(APIView):

	def get(self,request):
		phonenumber=request.GET.get('phonenumber')
		if not phonenumber: return Response({"message":"phonenumber is required"},400)
		try:
			User.objects.get(phonenumber=phonenumber)
		except:
			return Response({"message":"phonenumber not yet registered"},400)
		try:
			OtpView().send_otp(phonenumber)
		except Exception as err:
			return Response({"message":str(err)},400)
		return Response({"message":"otp sent successfully"},200)

	def post(self,request):
		phonenumber=request.data.get('phonenumber')
		otp=request.data.get('otp')
		password=request.data.get("password")
		if not phonenumber: return Response({"message":"phonenumber is required"},400)
		if not otp: return Response({"message":"otp is required"},400)
		if not password: return Response({"message":"password is required"},400)
		try:
			user=User.objects.get(phonenumber=phonenumber)
		except:
			return Response({"message":"phonenumber not yet registered"},400)
		try:
			temp=OtpView().validate_otp(phonenumber,otp)
			if not temp:
				return Response({"message":"Invalid Otp"},400)
		except Exception as err:
			return Response({"message":str(err)},400)
		user.set_password(password)
		user.save()
		return Response({"message":"password updated successfully"},200)

