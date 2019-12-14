from django.contrib import admin
from .models import Task, TaskAllocation

admin.site.register(Task)
admin.site.register(TaskAllocation)
