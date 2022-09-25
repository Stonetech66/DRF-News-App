from .models import CustomUsers
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=CustomUsers)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUsers)
def save_userprofile(sender, instance, created, **kwargs):
    instance.userprofile.save()