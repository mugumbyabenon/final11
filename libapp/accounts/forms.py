from django.contrib.auth.forms import UserCreationForm
from django import forms
from  django.db import transaction
from .models import User,Student,librarian
from django.db import IntegrityError
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    Student_number = forms.CharField(required=True)
    WebMail = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email= self.cleaned_data.get('WebMail')
        user.Reg=self.cleaned_data.get('Student_number')
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user
class librarainSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    Staff_number = forms.CharField(required=True)
    WebMail = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_librarian = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.Reg=self.cleaned_data.get('Staff_number')
        user.WebMail=self.cleaned_data.get('WebMail')
        user.save()
        lib = librarian.objects.create(user=user)
        lib.save()
        return user

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)