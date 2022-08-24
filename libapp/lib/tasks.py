from celery import shared_task
from .models import borrowed_books
from accounts.models import User
from libapp import settings
import datetime
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from django.utils import timezone
from datetime import timedelta

logger = get_task_logger(__name__)
@shared_task()
def thirty():
    logger.info('I run every 30 seconds')
    return 'Done'

@shared_task()
def send_notification():
    for x in borrowed_books.objects.all():
        z= User.objects.get(username=x.username)
        r = x.Return - datetime.timedelta(days=1)
        if datetime.date.today() == r.date():
            print(r)
            z.msg1 = True
            z.save()
            subject = 'Welcome to bookworld'
            message = "Hello " + z.first_name + '\n' + 'We are reminding you that your book is due for returning tomorrow\nThank for using bookworld '
            from_email = settings.EMAIL_HOST_USER
            to_list = [z.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
