from django import forms
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm


class UserCreationForm(BaseUserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','phone_number','date_of_birth','email', 'password1', 'password2')


class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','phone_number','date_of_birth','email', 'password')
    
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class OtpForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='OTP')


