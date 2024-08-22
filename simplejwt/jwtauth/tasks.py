from celery import shared_task
from .models import UserData
from django.core.mail import send_mail
from .auth import generate_otp
from django.conf import settings

@shared_task()
def reverse(text):
    print(f"reversing text: {text}")
    return text[::-1]


@shared_task
def send_mail_one(user_id):
    try:
        user = UserData.objects.get(id= user_id)
        otp = generate_otp()
        user.otp = otp
        user.save()
        send_mail(
                'Email Verification OTP',
                f'Your OTP for email verification is : {otp}',
                settings.EMAIL_HOST_USER,
                [ user.email],
                fail_silently = False
        )
        return user.email
   
    except UserData.DoesNotExist:
        return None



@shared_task(bind = True)
def send_mail_all(self):
    users = UserData.objects.all()
    for user in users:
        mail_subject = "32122242 this is from celery"
        message = "Completed through celery"
        email = user.email
        send_mail(
            subject = mail_subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
    return "OK"
