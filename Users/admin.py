from django.contrib import admin
from django.contrib import admin
from .models import  CustomUsers ,UserProfile
from django.contrib import admin
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model=CustomUsers
    list_display=["username", "email", "age"]
    list_filter=["gender", "country"]
    

admin.site.register(CustomUsers, CustomUserAdmin)
admin.site.register(UserProfile)

#admin.site.register(UserProfile)

