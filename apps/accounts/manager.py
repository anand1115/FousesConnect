from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):

	def create_user(self,first_name,last_name,phonenumber,email,password,admin=False,active=False):
		if not first_name:
			raise ValueError(_("First Name Is Required"))

		if not last_name:
			raise ValueError(_("Last Name Is Required"))

		if not phonenumber:
			raise ValueError(_("Phonenumber Is Required"))

		if not email:
			raise ValueError(_("Email Is Required"))

		if not password:
			raise ValueError(_("Password Is Required"))

		user=self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name,
						phonenumber=phonenumber,active=active,admin=admin)

		user.set_password(password)

		user.save(using=self._db)

		return user


	def create_superuser(self,first_name,last_name,phonenumber,email,password,admin=True,active=True):

		user=self.create_user(first_name,last_name,phonenumber,email,password,admin,active)
		
		return user