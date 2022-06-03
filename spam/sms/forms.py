from django import forms
from. models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')
        labels=('password1','password','password2','confirm_password')


class ProfileForm(forms.ModelForm):
    address=forms.Textarea()
    class Meta:
        model=Register
        fields=('address','phone_number')
class UploadForm(forms.ModelForm):
    spamtxt=forms.Textarea()
    class Meta:
        model=Upload
        fields=('spamtxt',)