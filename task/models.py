from django.db import models
from project.models import Project
from registration.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('underqa', 'Under QA'),
        ('underuat', 'Under UAT'),
        ('approved', 'Approved'),
        ('merged', 'Merged'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=20)
    description = models.TextField(blank=False, max_length=200)
    deadline = models.DateField(blank=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Created')
    weightage = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class TaskAllocation(models.Model):
    ROLE_CHOICES = [
        ('Developer', 'Developer'),
        ('UI Designer', 'UI Designer'),
        ('QA', 'QA'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='taskallocation')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=201, choices=ROLE_CHOICES)
    allocation = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.get_role_display()

