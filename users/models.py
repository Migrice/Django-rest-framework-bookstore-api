from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser

from commons.models import AbstractCustomModel

class User(AbstractBaseUser, AbstractCustomModel):
    username = models.CharField(null=False, blank=False, max_length=255, unique=True)
    email = models.EmailField(null=False, blank=False, max_length=255,unique=True)
    password = models.CharField(null=False, blank=False, max_length=255)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'


    objects = UserManager()

    class Meta:
        ordering = ['username']


