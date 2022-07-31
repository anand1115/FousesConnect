from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from .manager import MyUserManager

class User(AbstractBaseUser):
	id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
	first_name=models.CharField(max_length=250)
	last_name=models.CharField(max_length=250)
	phonenumber=models.CharField(max_length=15,unique=True)
	email=models.EmailField(max_length=250,unique=True)
	active=models.BooleanField(default=False)
	admin=models.BooleanField(default=False)
	added_on=models.DateTimeField(auto_now_add=True)
	verified=models.BooleanField(default=False)

	USERNAME_FIELD="phonenumber"

	REQUIRED_FIELDS=['email','first_name','last_name']

	objects=MyUserManager()

	def __str__(self):
		return self.phonenumber +"-"+self.first_name +" "+self.last_name

	@property
	def is_active(self):
		return self.active

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_staff(self):
		return self.admin

	def has_perm(self,perm,obj=None):
		return True

	def has_perms(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
		return True
	
	