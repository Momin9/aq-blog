from django.contrib import admin

from .models import UserBiography, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserBiography)
