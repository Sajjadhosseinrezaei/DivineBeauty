from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser, UserProfile
from order.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm, UserLoginForm, OtpForm, EmailForm, ProfileEditForm
from django.contrib import messages
from utility import redirect_with_next, OTPService
from django.contrib.auth.hashers import make_password
import time
import secrets
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.

class UserEmailVerificationView(View):
    form_class = EmailForm
    template_name = 'accounts/verify_email.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'شما قبلاً وارد شده‌اید.')
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
                messages.error(request, 'ایمیل قبلاً ثبت شده است.')
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
            messages.info(request, 'شما قبلاً وارد شده‌اید. ابتدا خارج شوید.')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            success , message = OTPService.verify_otp(request, form.cleaned_data['otp'])
            if success:
                request.session['registration_token'] = secrets.token_urlsafe(16)
                request.session['registration_token_created_at'] = timezone.now().isoformat()
                messages.success(request, 'message')
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
        registration_token = request.session.get('registration_token')
        token_created_at = request.session.get('registration_token_created_at')

        if not registration_token or not token_created_at:
            messages.error(request, 'دسترسی مستقیم به ثبت‌نام مجاز نیست.')
            return redirect('home:home')

        # اعتبار زمانی توکن (مثلا 15 دقیقه)
        created_time = timezone.datetime.fromisoformat(token_created_at)
        if timezone.now() - created_time > timezone.timedelta(minutes=15):
            messages.error(request, 'مدت زمان ثبت‌نام شما به پایان رسید.')
            request.session.pop('registration_token', None)
            request.session.pop('registration_token_created_at', None)
            return redirect('accounts:email_verify')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        email = request.session['user']['email']
        form = self.form_class(initial={'email': email})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            date_of_birth = form.cleaned_data['date_of_birth']
            user = CustomUser.objects.filter(email=email)
            if user.exists():
                messages.error(request, 'ایمیل قبلاً ثبت شده است.')
                return redirect('accounts:email_verify')

            password = form.cleaned_data['password1']
            user = CustomUser.objects.create_user(email=email,
                                                   password=password,
                                                   first_name=first_name,
                                                     last_name=last_name,
                                                         date_of_birth=date_of_birth)
            user.save()

            # پاک کردن session بعد از ثبت موفق
            request.session.pop('user', None)
            request.session.pop('registration_token', None)
            request.session.pop('registration_token_created_at', None)

            messages.success(request, "ثبت‌نام با موفقیت انجام شد!")
            login(request, user)
            return redirect('home:home')

        return render(request, self.template_name, {'form': form})

        

    

class UserLoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'شما قبلاً وارد شده‌اید.')
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
                if 'pending_add_to_cart' in request.session:
                    return redirect('order:resume_add_to_cart')
                
                messages.success(request, 'با موفقیت وارد شدید.')
                return redirect_with_next(request, default='home:home')
            else:
                messages.error(request, 'اطلاعات وارد شده نادرست است.')
        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'با موفقیت خارج شدید.')
        return redirect('home:home')
    



class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    form_class = ProfileEditForm

    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'برای دسترسی به این صفحه باید وارد حساب کاربری خود شوید.')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if not request.user.is_authenticated:
            self.profile = None
            self.orders = None
            self.user = None
            return
        self.profile = get_object_or_404(UserProfile, user=request.user)
        self.orders = Order.objects.filter(user=request.user)
        self.user = request.user

    def get(self, request, *args, **kwargs):
        
        user = request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'bio': self.profile.bio,
            'location': self.profile.location,
            'website': self.profile.website,
            # 'profile_picture': profile.profile_picture,  # معمولاً فایل‌ها را به صورت initial نمی‌گذارند
        }
        form = ProfileEditForm(initial=initial_data)
        orders = Order.objects.filter(user=user)
        return render(request, self.template_name, {
            'profile': self.profile,
            'orders': self.orders,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, self.template_name, {
                'profile': self.profile,
                'orders': self.orders,
                'user': self.user,
                'form': form,
            })
        # داده‌های تمیزشده را استفاده کنید
        cd = form.cleaned_data
        user = self.user
        user.first_name = cd['first_name']
        user.last_name = cd['last_name']
        user.date_of_birth = cd['date_of_birth']
        user.save()
        profile = self.profile
        profile.bio = cd['bio']
        profile.location = cd['location']
        profile.website = cd['website']
        if cd['profile_picture']:
            profile.profile_picture = cd['profile_picture']
        profile.save()
        messages.success(request, 'اطلاعات شما با موفقیت ثبت شد.')
        return redirect('accounts:profile')
        



class UserListCreateApiView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]



