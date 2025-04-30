from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_otp_email(subject, message, from_email, recipient_list):
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True, "کد ارسال شد. ایمیل خود را چک کنید."
    except Exception as e:
        return False, f'ارسال OTP با خطا مواجه شد: {str(e)}'