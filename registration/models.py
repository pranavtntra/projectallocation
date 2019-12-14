from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    name = models.CharField(blank=False, max_length=20)
    percentage = models.IntegerField(blank=True, default=0)
    phone = PhoneNumberField(blank=True, null=True)
    verification = models.BooleanField(default=False)

    def __str__(self):
        return self.username + " Allocation: " + str(self.percentage) + "%"

    def __unicode__(self):
        return self.name

    @classmethod
    def user_query(cls):
        context = {'allusers': cls.objects.all()}
        return context



