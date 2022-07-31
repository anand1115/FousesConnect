from django.db import models
from apps.accounts.models import User
import uuid
# Create your models here.



class UserDetail(models.Model):
	id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	city=models.CharField(max_length=200,blank=True)
	state=models.CharField(max_length=200,blank=True)
	aadhar_number=models.CharField(max_length=200,blank=True)
	pan_number=models.CharField(max_length=200,blank=True)
	gstin_id=models.CharField(max_length=200,blank=True)
	step=models.PositiveIntegerField(default=0)
	rzrp_id=models.CharField(max_length=200,blank=True)
	rzrp_details=models.JSONField(default=dict,blank=True)


	def __str__(self):
		return self.user.first_name+" "+self.user.last_name


