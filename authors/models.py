from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', primary_key=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    dob = models.DateField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    currently_learning = models.TextField(blank=True)
    skills_language = models.TextField(blank=True)
    currently_hacking_on = models.TextField(blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    education = models.TextField(blank=True)
    work = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class UserBiography(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="user_biography")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(upload_to="biography/profile/", blank=True)
    university_designation = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    other_designation = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    biography = models.TextField(blank=True)
    skills_and_expertise = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Get first_name, last_name, and profile_image from related models
        self.first_name = self.user_profile.user.first_name
        self.last_name = self.user_profile.user.last_name
        self.profile_image = self.user_profile.profile_image
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_profile.user.username}'s biography"
