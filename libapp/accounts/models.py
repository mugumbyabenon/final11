from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User
from django.contrib.auth.models import UserManager
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True,primary_key=True)
    password = models.CharField(max_length=30)
    is_student = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default=True)
    Reg = models.CharField(max_length=100,default=True,null=False)
    books_borrowed = models.IntegerField(default=0)
    fine = models.BooleanField(default=False)
    total = models.IntegerField(default=0)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=True)

class librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=True)




