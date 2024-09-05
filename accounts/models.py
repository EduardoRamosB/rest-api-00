from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
        ('adopter', 'Adopter'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='adopter')

    def __str__(self):
        return self.email
