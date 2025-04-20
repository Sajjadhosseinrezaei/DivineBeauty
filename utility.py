from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.db import models
from slugify import slugify
import secrets
import  bcrypt
from django.core.mail import send_mail
import time
from django.contrib import messages




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




class OTPService:
    MAX_ATTEMPTS = 5
    ATTEMPT_RESET_SECONDS = 300  # 5 دقیقه
    OTP_EXPIRE_SECONDS = 120  # 2 دقیقه


    @staticmethod
    def generate_and_store_otp(request, email):
        # تولید OTP و هش کردن آن
        code = OTPManager.generate_otp()
        hashed_code = OTPManager.hash_otp(code)

        # ذخیره OTP و زمان تولید آن در سشن
        session = request.session.get('user', {})
        session['otp'] = hashed_code
        session['otp_timestamp'] = time.time()
        session['otp_attempts'] = 0
        session['otp_attempt_time'] = time.time()

        # بروزرسانی سشن
        request.session['user'] = session
        request.session.modified = True
        return code

    @staticmethod
    def send_otp_via_email(email, otp_code):
        # ارسال کد OTP به ایمیل
        subject = 'Your OTP Code'
        message = f'Your OTP code is: {otp_code}'
        from_email = 'your_email@example.com'  # آدرس ایمیل خود را وارد کن
        try:
            send_mail(subject, message, from_email, [email])
            return True , "code send check your email"
        except Exception as e:
            return False, 'Failed to send OTP: {str(e)}'


    @staticmethod
    def verify_otp(request, user_input_otp):
        session = request.session.get('user')
        if not session:
            return False, "Session expired or not found."

        now = time.time()
        otp_timestamp = session.get('otp_timestamp')
        if not otp_timestamp or now - otp_timestamp > OTPService.OTP_EXPIRE_SECONDS:
            return False, "OTP has expired. Please request a new one."
        # مدیریت ریست تعداد تلاش‌ها
        if 'otp_attempt_time' in session and now - session['otp_attempt_time'] > OTPService.ATTEMPT_RESET_SECONDS:
            session['otp_attempts'] = 0
            session['otp_attempt_time'] = now

        if session.get('otp_attempts', 0) >= OTPService.MAX_ATTEMPTS:
            return False, "Too many attempts. Try again 5 minuts later."

        stored_hashed_otp = session.get('otp')
        if not stored_hashed_otp:
            return False, "OTP not found in session."

        # تایید OTP وارد شده
        if OTPManager.verify_otp(user_input_otp, stored_hashed_otp):
            # موفقیت، پاک کردن OTP از سشن
            del session['otp']
            del session['otp_timestamp']
            session['otp_attempts'] = 0
            request.session.modified = True
            return True, "OTP verified successfully."
        else:
            session['otp_attempts'] = session.get('otp_attempts', 0) + 1
            session['otp_attempt_time'] = now
            request.session['user'] = session
            request.session.modified = True
            return False, "Invalid OTP."
        


    @staticmethod
    def resend_otp(request):
        session = request.session.get('user')
        if not session:
            return False, "Session not found. Please start the verification process again."

        email = session.get('email')
        if not email:
            return False, "Email not found in session."

        # بررسی زمان ریست تلاش‌ها
        now = time.time()
        last_attempt_time = session.get('otp_attempt_time', 0)
        if now - last_attempt_time > OTPService.ATTEMPT_RESET_SECONDS:
            # اگر بیشتر از ۵ دقیقه گذشته باشد، تعداد تلاش‌ها ریست می‌شود
            session['otp_attempts'] = 0

        # بررسی محدودیت زمانی برای ارسال دوباره
        last_sent_time = session.get('otp_timestamp', 0)
        if now - last_sent_time < 120:  # تغییر زمان به 60 ثانیه
            return False, "Please wait a minute before requesting another OTP."

        # بررسی تعداد تلاش‌ها
        if session.get('otp_attempts', 0) >= OTPService.MAX_ATTEMPTS:
            return False, "You have reached the maximum number of OTP requests. Please try again 5 minuest later."

        # افزایش تعداد تلاش‌ها
        session['otp_attempts'] = session.get('otp_attempts', 0) + 1
        session['otp_attempt_time'] = now

        # تولید و ذخیره کد OTP جدید
        code = OTPManager.generate_otp()
        hashed_code = OTPManager.hash_otp(code)

        session['otp'] = hashed_code
        session['otp_timestamp'] = now  # بروزرسانی زمان ارسال OTP
        request.session['user'] = session
        request.session.modified = True

        # ارسال ایمیل
        try:
            OTPService.send_otp_via_email(email, code)
        except Exception as e:
            return False, f"Failed to send OTP: {str(e)}"

        return True, "A new OTP has been sent to your email."



