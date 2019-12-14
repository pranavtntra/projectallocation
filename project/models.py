from django.db import models
from registration.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ('underprogress', 'Under progress'),
        ('created', 'Created'),
        ('closed', 'Closed'),
    ]
    name = models.CharField(blank=False, max_length=20, unique=True)
    description = models.TextField(blank=False, max_length=200)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='created')

    def __str__(self):
        return self.name
    @staticmethod
    def project_query():
        context = {'allprojects': Project.objects.all()}
        return context


class Teamlead(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name


class ProjectAllocation(models.Model):
    ROLE_CHOICES = [
        ('Developer', 'Developer'),
        ('UI Designer', 'UI Designer'),
        ('QA', 'QA'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=201, choices=ROLE_CHOICES)
    allocation = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.get_role_display()



    # def clean_email(self):
    #     allocation = self.cleaned_data['allocation']
    #
    #     if email.endswith('@cowhite.com'):
    #         raise ValidationError('Domain of email is not valid')
    #
    #     return email