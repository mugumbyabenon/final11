from django.db import models
import datetime
from libapp import settings
from django.core.mail import send_mail
from accounts.models import User
from django.urls import reverse
from django.db.models import Max,F

# Create your models here.
class lib(models.Model):
    Book_name = models.CharField(max_length=30)
    Book_author = models.CharField(max_length=30)
    Book_number = models.AutoField(auto_created=True,primary_key=True,editable=False,blank=True )
    Book_shelf = models.CharField(max_length=30)
    Number_of_available_copies = models.PositiveIntegerField(blank=False,null=True,default=0)
    Date_added = models.DateTimeField(auto_now_add=True, blank=True)
    Book_category = models.CharField(max_length=30)
    isbn = models.CharField('ISBN', max_length=13,default=False)
    pic = models.ImageField(blank=True, null=True, upload_to='images/')
    n = models.CharField(max_length=25, default=True)
    summary = models.TextField(default=False)

class borrowed_books(models.Model):
    book_title=models.CharField(max_length=30)
    username = models.CharField(max_length=100,default=True)
    borrower_fname = models.CharField(max_length=30,default=True)
    borrower_lname = models.CharField(max_length=30,default=False)
    borrower_number = models.CharField(max_length=30,default=False)
    book_number = models.CharField(max_length=30, default=False)
    date = models.DateTimeField(default=True)
    Return = models.DateTimeField(default=True)
    fine = models.IntegerField(default=0)
    q = models.AutoField(auto_created=True,primary_key=True,editable=False)







