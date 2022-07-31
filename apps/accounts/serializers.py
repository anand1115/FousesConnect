from .models import *
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
import jwt




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        extra_kwargs = {
            "first_name": {
                "error_messages": {
                    "required": "first name is required"
                }
            },
            "last_name": {
                "error_messages": {
                    "required": "last name is required"
                }
            },
            "phonenumber": {
                "error_messages": {
                    "required": "Mobile Number is required"
                }
            },
            "email": {
                "error_messages": {
                    "required": "email is required"
                }
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
    def validate_first_name(self,first_name):
        if(not 3<len(first_name)<100):
            raise serializers.ValidationError("Invalid First Name.")
        return first_name

    def validate_last_name(self,last_name):
        if(not 3<len(last_name)<100):
            raise serializers.ValidationError("Invalid last Name.")
        return last_name
    
    def validate_phonenumber(self,phonenumber):
        try:
            User.objects.get(phonenumber=phonenumber)
            raise serializers.ValidationError("phonenumber already exist")
        except:
            pass
        if(not phonenumber.isdigit() or len(phonenumber)!=10):
            raise serializers.ValidationError("Invalid Phone Number.")
        return phonenumber
        
    def validate_email(self,email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError("email already exist")
        except:
            pass
        if not 3<=len(email)<=50:
            raise serializers.ValidationError("Invalid email !")
        return email

    def create(self,data):
        return User.objects.create(**data)
class CustomTokenObtainPairSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        temp=jwt.decode(data['access'],'FousesConnect', algorithms=["HS256"])
        user=User.objects.get(phonenumber=temp['phonenumber'])
        data['data']=UserSerializer(user).data
        return data