from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    long_description = models.TextField(max_length=1000, default=True)
    image = models.ImageField(upload_to='media/')
    date_created = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'newsEvents'

class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'client'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.username

    # Create a user profile by default when user signups
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

    # Automate the profile
post_save.connect(create_profile, sender=User)

class InterpreterApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    county = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField()
    languages = models.TextField()
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="media/")
    profile_image = models.ImageField(upload_to='interpreters/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # social media platform
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}- {self.status}"

class EducationalResource(models.Model):
    CATEGORY_CHOICES = [
        ('sign-language', 'Sign Language'),
        ('deaf-history', 'Deaf History'),
        ('education', 'Education Materials'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='media/', blank=True, null=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # For external resources

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Interpretation(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('physical', 'Physical Interpretation'),
        ('virtual', 'Virtual Interpretation'),
    ]

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="media/")

    def __str__(self):
        return self.get_service_type_display()

class CommunityGroup(models.Model):
    PLATFORM_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('telegram', 'Telegram'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=255)  # Group Name
    link = models.URLField()  # Group Link
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)  # Platform Type
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField(max_length=500)

    def __str__(self):
        return self.question
