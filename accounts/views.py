from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm, UserLoginForm
from django.contrib import messages
from utility import redirect_with_next
# Create your views here.

class UserCreationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    model = CustomUser
    success_url =  reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created and logged in.')
        return redirect_with_next(self.request, default=self.success_url)



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