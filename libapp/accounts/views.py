from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import StudentSignUpForm,librarainSignUpForm,ContactForm
from .models import User,librarian,Student
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.decorators import login_required,user_passes_test
from libapp import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .token import generate_token
from django.conf import settings
from lib.models import lib
#from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.models import User

# Create your views here.
def register(request):
    return render(request, '../templates/registeruser.html')

@user_passes_test(lambda u: u.is_staff)
def librarain(request):
    queryset = lib.objects.all()
    return render(request, '../templates/librarain.html',{'queryset':queryset} )

@user_passes_test(lambda u: u.is_student)
def student(request):
    queryset = lib.objects.all()
    return render(request, '../templates/student.html',{'queryset':queryset} )

@user_passes_test(lambda u: u.is_superuser)
def librarain_register(request):
    if request.method == 'POST':
        username = request.POST['register']
        try:
            n = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.success(request,'The specified user name doesnot exist')
            return redirect('/accounts/librarain_register/')
        if n.is_student == True:
            n.is_student = False
            n.is_staff = True
            n.is_email_verified = False
            n.save()
            messages.success(request,'The user is now a librarain')
            return redirect('/accounts/login/')
        else:
            n.is_student = True
            n.is_staff = False
            n.is_email_verified = False
            n.save()
            messages.success(request, 'The user is no longer now a librarain and now a student')
            return redirect('/accounts/login/')

    return render(request,'libform.html')

def send_email(request,user,message):
    myuser= user
    current_site = get_current_site(request)
    email_subject = message
    message2 = render_to_string("email_confirmation.html", {
        'name': myuser.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(myuser.username)),
        'token': generate_token.make_token(myuser)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
    )
    email.fail_silently = False
    email.send()
    return redirect('/accounts/login/')

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            if not user.is_email_verified:
                user=request.user
                title = 'Your account is not yet verified\n, check your Webmail for verification token or request for another token by clicking Resend button'
                return render(request,'resend.html',{'title':title})
            else:
                if user is not None:
                   if user.is_staff:
                        login(request, user)
                        return redirect('/accounts/librarain/')
                   else:
                       login(request, user )
                       return redirect(('/accounts/student/'))
        else:
                messages.success(request, 'Invalid username or password')
                return render(request, '../templates/login.html')
    else:
       return render(request, 'login.html', {'title':'Welcome to the login page'})

def logout_view(request):
    logout(request)
    return redirect('/')



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['username']
        reg = request.POST['reg']
        if User.objects.filter(username=username):
            messages.error(request,'Username already exists Please try some other username')
            return redirect('/accounts/signup/')
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists Please try some other email')
            return redirect('/accounts/signup/')
        if pass1 == pass2:
            messages.error(request, 'Passwords didnt match')
            return redirect('/accounts/signup/')
        if User.objects.filter(Reg=reg):
            messages.error(request,'Registration already exists Please try some other Registration number')
            return redirect('/accounts/signup/')
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.Reg = reg
        myuser.is_email_verified = False
        myuser.save()
        login(request,myuser)
        messages.success(request,'An activation token has been sent to your webmail or click Resend to resend token')
        #Welcome email
        subject = 'Welcome to bookworld'
        message = "Hello "+ myuser.first_name+'\n'+'Thank for using bookworld\n We have sent you a confirmation link\nPlease activate your account'
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        #Email Address Confirmation Email
        n = 'Confirm your password using the link below'
        send_email(request,myuser,n)
        return render(request,'resend.html')
    return render(request,'signup.html')

def resend(request):
    user = request.user
    try:
        if  user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Account already verified')
            return redirect('/accounts/login/')
        else:
            n = 'Account activation link'
            send_email(request, user, n)
            messages.add_message(request, messages.ERROR, 'Token resent check your webmail')
            return redirect('/accounts/login/')
    except AttributeError:
        n = 'Confirm your account using the link below'
        send_email(request, user, n)
        messages.add_message(request, messages.ERROR, 'Token resent check your webmail')
        return redirect('/accounts/login/')


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(username=uid)
    except (TypeError, ValueError, OverflowError):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_email_verified = True
        myuser.is_student = True
        myuser.save()
        login(request, myuser)
        if myuser.is_superuser:
            return redirect('/accounts/librarain/')
        else:
            return redirect('/accounts/student/')

    else:
        return render(request, 'activation_failed.html')