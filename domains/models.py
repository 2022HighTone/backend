from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class UserManager (BaseUserManager) :
    
    def create_user (self, username, email, password=None) :

        if username is None :
            raise TypeError('Users should have a username')

        if email is None :
            raise TypeError('Users should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser (self, username, email, password=None) :

        if password is None :
            raise TypeError('Password should not be none')

        user = self.create_user(
            username,
            email,
            password,
        )
        
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User (AbstractBaseUser, PermissionsMixin) :
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__ (self) :
        return self.email


class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=256)


class Store(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    address = models.CharField(null=True, blank=True, max_length=512)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)