from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.db import models
from slugify import slugify
import secrets
import  bcrypt
from django.core.mail import send_mail




def redirect_with_next(request, default='/', param_name='next'):
    """
    Redirects user to a safe 'next' URL if available, otherwise to default.

    Args:
        request: The current HttpRequest object.
        default: The fallback URL to redirect if next is invalid or missing.
        param_name: The GET or POST param to check for next URL (default is 'next').

    Returns:
        HttpResponseRedirect
    """
    next_url = request.GET.get(param_name) or request.POST.get(param_name)
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect(default)



class AutoSlugField(models.SlugField):
    """
    A custom SlugField that automatically generates a slug from the name field
    if the slug field is empty.
    """
    def pre_save(self, model_instance, add):
        slug = getattr(model_instance, self.attname)
        if not slug:
            base_value = getattr(model_instance, 'name', None)  # از name می‌سازه
            if base_value:
                slug = slugify(base_value, allow_unicode=True) # ساخت اسلاگ فارسی
                setattr(model_instance, self.attname, slug)
        return slug
    



class OTPManager:
    @staticmethod
    def generate_otp(length=6):
        return ''.join(secrets.choice('0123456789') for _ in range(length))

    @staticmethod
    def hash_otp(otp):
        return bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()  # خروجی string

    @staticmethod
    def verify_otp(otp, otp_hash):
        return bcrypt.checkpw(otp.encode(), otp_hash.encode())  # هر دو bytes





def send_otp_via_email(email, otp):
    """
    Sends the OTP to the user's email address.

    Args:
        email: The user's email address.
        otp: The OTP to send.

    Returns:
        None
    """
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = 'sajjadhosseinrezay6@gmail.com'  # Replace with your email address
    recipient_list = [email] # List of recipient email addresses
    send_mail(subject, message, from_email, recipient_list)