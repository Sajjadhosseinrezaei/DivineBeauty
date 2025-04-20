from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm, UserLoginForm, OtpForm, EmailForm
from django.contrib import messages
from utility import redirect_with_next, OTPService
from django.contrib.auth.hashers import make_password
import time
# Create your views here.


class UserEmailVerificationView(View):
    form_class = EmailForm
    template_name = 'accounts/verify_email.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    

    def post(self, request):
        form = self.form_class(request.POST)
        request.session.pop('user', None)
        if form.is_valid():
            email = form.cleaned_data['email']

            # بررسی وجود ایمیل بدون حساسیت به حروف بزرگ و کوچک
            if CustomUser.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('accounts:email_verify')

            # ساخت ساختار session به صورت امن
            user_session = request.session.get('user', {})
            user_session['email'] = email


            # ذخیره اطلاعات جدید در session
            # ذخیره user_session و OTP در سشن
            request.session['user'] = user_session
            request.session.modified = True

            # ارسال و ذخیره OTP
            code = OTPService.generate_and_store_otp(request, request.session['user']['email'])
            success , message = OTPService.send_otp_via_email(request.session['user']['email'], code)
            if success:
                messages.success(request, message)
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, message)
                return redirect('accounts:email_verify')

        return render(request, self.template_name, {'form': form})

                
class UserOtpVerificationView(View):
    template_name = 'accounts/verify_otp.html'
    form_class = OtpForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in first log out.')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            success , message = OTPService.verify_otp(request, form.cleaned_data['otp'])
            if success:
                messages.success(request, message)
                return redirect('accounts:register')
            else:
                messages.error(request, message)
                return redirect('accounts:verify_otp')
            
        return render(request, self.template_name, {'form':form})
    
class ResendOTPView(View):
    def post(self, request):
        success, message = OTPService.resend_otp(request)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('accounts:verify_otp')



class UserCreationView(View):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in first logout.')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
 
    def get(self, request):
        email = request.session['user']['email']
        form = self.form_class(initial={'email':email})
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email)
            if user.exists():
                messages.error(request, 'Email already exists.')
                return redirect('accounts:email_verify')
            password = form.cleaned_data['password1']
            user = CustomUser.objects.create_user(email=email, password=password)
            user.save()
            request.session.pop('user', None)
            messages.success(request, "user created and login")
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect_with_next(request, default='home:home')
        
        return render(request, self.template_name, {'form':form})
        
        

    

class UserLoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect_with_next(request, default='home:home')
            else:
                messages.error(request, 'Invalid credentials.')
        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home:home')