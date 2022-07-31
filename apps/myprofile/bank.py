from django.conf import settings
from .models import *
import razorpay
import random
key_id=settings.RAZORPAY_KEY_ID
secret_id=settings.RAZORPAY_KEY_SECRET
client = razorpay.Client(auth=(key_id,secret_id))
client.set_app_details({"title" : "django", "version" : "3.2.8"})

class VirtualBank:

	def __init__(self,user):
		self.user=user

	def create(self):
		cust_id,status=self.get_customer()
		if not status:
			return cust_id,False
		try:
			data=client.virtual_account.create({
			  "receivers": {
			    "types": [
			      "bank_account",
			      "vpa"
			    ],
			    "vpa":{
				   "descriptor": (str(random.randint(10,99))+self.user.first_name+self.user.last_name)[:10]
				}
			  },
			  "description": f"Virtual Account created for {self.user.first_name} {self.user.last_name}",
			  "customer_id": cust_id,
			  "notes": {
			    "user_id": str(self.user.id)
			  }
			})
			return (data,True)
		except Exception as err:
			return (str(err),False)


	def get_customer(self):
		details,status=UserDetail.objects.get_or_create(user=self.user)
		if(details.rzrp_id):
			return details.rzrp_id,True
		else:
			try:
				data=client.customer.create({
				  "name": self.user.first_name+" "+self.user.last_name,
				  "contact":self.user.phonenumber,
				  "email": self.user.email,
				  "fail_existing": 0,
				  "gstin": details.gstin_id,
				})
				details.rzrp_id=data['id']
				details.save()
			except Exception as err:
				return str(err),False
			return details.rzrp_id,True

	def get_payments(self):
		details,status=self.get_virtual_account()
		if status:
			try:
				data=client.virtual_account.payments(details['id'])
			except Exception as err:
				return str(err),False
			return data,True
		else:
			return "Create Virtual Account First",False

	def get_virtual_account(self):
		details,status=UserDetail.objects.get_or_create(user=self.user)
		if(details.rzrp_id):
			return details.rzrp_details,True
		else:
			return details.rzrp_details,False




