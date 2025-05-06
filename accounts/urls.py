from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('email/verify/', views.UserEmailVerificationView.as_view(), name='email_verify'),
    path('verify/otp/', views.UserOtpVerificationView.as_view(), name='verify_otp'),
    path('resend/otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    path('register/', views.UserCreationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('api/users/', views.UserListCreateApiView.as_view(), name='users'),
]