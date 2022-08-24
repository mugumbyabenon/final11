from celery import shared_task
from libapp import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .token import generate_token
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from django.shortcuts import  redirect,render
from .models import User
from django.contrib.auth import login

@shared_task(bind=True)
def welcome_email(self,myuser):
    subject = 'Welcome to bookworld'
    message = "Hello " + myuser.first_name + '\n' + 'Thank for using bookworld\n We have sent you a confirmation link\nPlease activate your account'
    from_email = settings.EMAIL_HOST_USER
    to_list = [myuser.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)

