from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

app_name="accounts"

urlpatterns=[
	path('login/',LoginView.as_view(),name="login"),
	path('signup/',SignupView.as_view(),name="signup"),
	path('otp_verify/',OtpVerifyView.as_view(),name="verify"),
	path('forgot_password/',ForgotPasswordView.as_view(),name="forgot"),
	path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]