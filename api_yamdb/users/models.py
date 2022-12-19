from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        USER='user'
        MODERATOR='moderator'
        ADMIN='admin'
    
    username=models.CharField(max_length=150,unique=True)
    email=models.EmailField(max_length=254, unique= True)
    first_name=models.CharField(max_length=150,blank=True)
    last_name=models.CharField(max_length=150,blank=True)
    bio=models.TextField(blank=True)
    role=models.CharField(max_length=10,choices=Role.choices,default=Role.USER)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    confirmation_code=models.CharField(max_length=150,blank=True)

    USERNAME_FIELD='username'

    REQUIRED_FIELDS=['email']
    
    objects=CustomUserManager()

    def __str__(self):
        return self.username
    


