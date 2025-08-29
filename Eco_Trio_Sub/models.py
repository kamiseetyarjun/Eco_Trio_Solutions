from django.db import models
from django.core.validators import RegexValidator

class Registration(models.Model):
    """
    Model for storing details from the EcoTrio popup registration form.
    This is intended for capturing customer inquiries, not for user accounts.
    """
    username = models.CharField(
        max_length=150,
        help_text="The full name or username of the user.",
        default="Anonymous"
    )
    email = models.EmailField(
        help_text="The user's email address.",
        null=True,
        blank=True
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text="The user's phone number.",
        default="0000000000"
    )

    occupation = models.CharField(
        max_length=100,
        help_text="The user's occupation.",
        default="Not specified"
    )
    interest = models.CharField(
        max_length=100,
        help_text="The user's area of interest from the dropdown.",
        default="Not specified"
    )
    looking_for = models.TextField(
        help_text="A brief description of what the user is looking for.",
        default="Not specified"
    )

    signup_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username if self.username else "Unnamed User"
    

from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')  # uploaded to MEDIA_ROOT/team/

    def __str__(self):
        return self.name


class Collaboration(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='collaborations/')  # Store images in MEDIA_ROOT/collaborations
    website_link = models.URLField(blank=True, null=True)
    #github_link = models.URLField(blank=True)
    # linkedin_link = models.URLField(blank=True)
    # twitter_link = models.URLField(blank=True)
    # instagram_link = models.URLField(blank=True)
    # facebook_link = models.URLField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='job_icons/')  # optional field
    description = models.TextField()

    def __str__(self):
        return self.title