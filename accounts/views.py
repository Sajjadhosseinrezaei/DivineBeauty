from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm, UserLoginForm, OtpForm
from django.contrib import messages
from utility import redirect_with_next, OTPManager, send_otp_via_email
from random import randint
# Create your views here.

class UserCreationView(View):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
 
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if not request.session.get('user'):
            request.session['user'] = {}
        if form.is_valid():
            request.session['user']['email'] = form.cleaned_data['email']
            request.session['user']['password'] = form.cleaned_data['password1']
            code = OTPManager.generate_otp()
            hashed_code = OTPManager.hash_otp(code)
            send_otp_via_email(request.session['user']['email'], code)
            request.session['user']['otp'] = hashed_code
            request.session.modified = True
            messages.success(request, 'Registration successful. Please verify your email.')
            return redirect('accounts:verify')
        return render(request, self.template_name, {'form': form})
        

class UserVerificationView(View):
    template_name = 'accounts/verify.html'
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
            otp = form.cleaned_data['otp']
            otp_user = request.session['user']['otp']
            if OTPManager.verify_otp(otp, otp_user):
                user = CustomUser.objects.create_user(
                    email=request.session['user']['email'],
                    password=request.session['user']['password']
                )
                user.save()
                del request.session['user']
                messages.success(request, 'User created successfully.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('accounts:verify')
        return render(request, self.template_name, {'form': form})
        

    

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
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home:home')