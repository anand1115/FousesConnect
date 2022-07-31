from django.urls import path
from .views import *

app_name="myprofile"

urlpatterns=[
	path("step1/",Step1FormView.as_view(),name="step1"),
	path("step2/",Step2FormView.as_view(),name="step2"),
	path("mybank/",VirtualBankView.as_view(),name="bank"),
]