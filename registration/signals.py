from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from majorproject.settings import EMAIL_HOST_USER


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Your account has been created",
            "Hello "
            + instance.name
            + ","
            + "\n"
            + "Your login credentials are: "
            + "\n"
            + "1. Username: "
            + instance.username
            + "\n"
            + "2. Password: "
            + instance.username
            + "@123"
            + "\n"
            + "A verification mail will be sent to you shortly."
            + "\n"
            + "Please verify as soon as you recieve",
            EMAIL_HOST_USER,
            [instance.email],
        )
