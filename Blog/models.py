from django.db import models
import Blogappx.settings
from django.urls import reverse
from django.conf import settings
from Users.models import CustomUsers
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
# Create your models here.

class Category(models.Model):
	name= models.CharField(max_length= 19, unique=True, null=True)
	slug= models.SlugField(max_length= 19, unique=True)

	def clean(self):
		if Category.objects.filter(name__iexact=self.name):
			raise ValidationError({"name":"Category already exits"})


	def save(self, *args, **kwargs): 
		self.slug = slugify(self.name) 
		super().save(*args, **kwargs) 
		pass 

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('ArticleListview')
	
	
	



class Article(models.Model):
	Author= models.ForeignKey( CustomUsers, on_delete=models.CASCADE, related_name="userarticle")
	date_published= models.DateTimeField(auto_now_add= True)
	title= models.CharField(max_length= 10000, unique=True)
	snippet= models.CharField(max_length= 10000)
	Category= models.ManyToManyField(Category , related_name="category", default= "coding")
	body= models.TextField()
	header_image= models.ImageField(null= True, blank= True, upload_to= "images/")

	

	class Meta:
		permissions= [("special_articlecreate", "can create Article"),]
		ordering= ['-date_published']
	

	
	def save(self, *args, **kwargs):
		self.slug=slugify(self.title)
		return super().save(*args, **kwargs)

	def clean(self):
		if Article.objects.filter(title__iexact=self.title):
			raise ValidationError({"name":"Article already exits"})

	def __str__(self):
		return f"{self.title[:20]}"

	def get_absolute_url(self):
		return reverse('ArticleDetailview', args=[str(self.id)])






class Comment(models.Model):
	Article= models.ForeignKey(Article, on_delete=models.CASCADE, related_name= "comments")
	name= models.ForeignKey(CustomUsers, on_delete=models.CASCADE, related_name="user_comments")
	comment= models.TextField(blank= False, null= False)
	date_published= models.DateTimeField(auto_now_add= True)

	
	class Meta:
		ordering= ['-date_published']

	def __str__(self):
		return f"{self.Article}-{self.comment [:27]}"


class Reply(models.Model):
	Comment= models.ForeignKey(Comment, on_delete=models.CASCADE ,related_name="replies")
	body= models.TextField()
	date_published= models.DateTimeField(auto_now_add= True)
	name= models.ForeignKey(CustomUsers, on_delete=models.CASCADE, related_name="replies")

	class Meta:
		ordering= ['-date_published']

	def __str__(self):
		return self.body[:20]


	

