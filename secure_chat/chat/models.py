from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)  # Required
    last_name = models.CharField(max_length=150, blank=True)  # Optional
    username = models.CharField(max_length=150, unique=True)  # Must be unique
    email = models.EmailField(null=True, blank=True)  # Allow duplicates
    password = models.CharField(max_length=255)  # Encrypted automatically

    def __str__(self):
        return self.username  # Display username when printing the object

