from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from authors.models import UserProfile

user = get_user_model()


@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
