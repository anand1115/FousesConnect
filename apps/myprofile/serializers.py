from .models import *
from rest_framework import serializers



class UserDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model=UserDetail
		exclude=['user']

	def to_representation(self,instance):
		data=super().to_representation(instance)
		data['first_name']=instance.user.first_name
		data['last_name']=instance.user.last_name
		data['email']=instance.user.email
		data['phonenumber']=instance.user.phonenumber
		return data