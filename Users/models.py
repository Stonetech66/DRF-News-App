from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, date
from dateutil.relativedelta import *
from django.core.exceptions import ValidationError

from Blog.countries import Countries


Genders=[
	("Male", "Male"),
	("Female", "Female"),
	("others", "others"),
	("Prefer not to say", "Prefer not to say")
]
# Create your models here.



class CustomUsers(AbstractUser):
	username= models.CharField(max_length=36, unique=True, error_messages={"username":"This username is taken"})
	email= models.EmailField(unique=True)
	Fullname= models.CharField( max_length=30)
	gender=models.CharField(max_length=20, choices=Genders)
	Birth_date= models.DateField(null=True , blank=False )
	country=models.CharField(max_length=100000, choices=Countries)
	
	@property
	def age(self):
		x=  relativedelta(date.today(),self.Birth_date)
		return x.years

	def get_absolute_url(self):
		return reverse('users-profile', kwargs= {"pk": self.pk})


	"""
	def clean(self) :
		if  (date.today()- self.Birth_date)//timedelta(days=365.2425) <=5 :
			raise ValidationError({"Birth_date":"invalid birthdate"})"""


class UserProfile(models.Model):
	user= models.OneToOneField(CustomUsers, on_delete=models.CASCADE, related_name="userprofile")
	bio= models.TextField()
	profile_pic= models.ImageField(upload_to= "./images", blank= True, null=True)
	verified= models.BooleanField(default=False)



	def __str__(self):
		return f"{self.user.username}"

	def get_absolute_url(self):
		return reverse("userprofile", kwargs={"pk": self.pk})

		
		
		
		



