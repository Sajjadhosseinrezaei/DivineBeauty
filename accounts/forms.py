from django import forms
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm


from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(BaseUserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'email', 'password1', 'password2')
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'date_of_birth': 'تاریخ تولد',
            'email': 'ایمیل',
            'password1*': '*گذرواژه',
            'password2*': '*تأیید گذرواژه'
        }
        help_texts = {
            'first_name': 'لطفاً نام خود را وارد کنید.',
            'last_name': 'لطفاً نام خانوادگی خود را وارد کنید.',
            'date_of_birth': 'لطفاً تاریخ تولد خود را وارد کنید.',
            'email': 'لطفاً ایمیل خود را وارد کنید.',
            'password1': 'گذرواژه باید حداقل ۸ کاراکتر باشد.',
            'password2': 'تأیید گذرواژه باید با گذرواژه وارد شده همخوانی داشته باشد.'
        }



class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','date_of_birth','email', 'password')
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')


class EmailForm(forms.Form):
    email = forms.EmailField(required=True, label='ایمیل', widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید', 'class': 'form-control'}))

class OtpForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='کد تایید')





class ProfileEditForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='نام',
        error_messages={'required': 'لطفاً نام را وارد کنید.'}
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='نام خانوادگی',
        error_messages={'required': 'لطفاً نام خانوادگی را وارد کنید.'}
    )
    date_of_birth = forms.DateField(
        required=False,
        label='تاریخ تولد',
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'invalid': 'فرمت تاریخ تولد صحیح نیست.'}
    )
    bio = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='بیوگرافی'
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        label='مکان'
    )
    website = forms.URLField(
        required=False,
        label='وبسایت',
        error_messages={'invalid': 'آدرس وبسایت معتبر نیست.'}
    )
    profile_picture = forms.ImageField(
        required=False,
        label='عکس پروفایل'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['rows'] = 3
            else:
                field.widget.attrs['class'] = 'form-control'



