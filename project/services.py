from .models import Project, ProjectAllocation, Teamlead
from .forms import Allocateemployeesssform
from registration.models import User
from task.models import Task, TaskAllocation
from django.shortcuts import render, redirect, get_object_or_404
import json

def projectview_query(project,lead, name, description, start_date, end_date, status):
    Teamlead.objects.create(project_id=int(project), user_id=int(lead))
    Project.objects.create(name=name, description=description,
                           status=status, start_date=start_date,
                           end_date=end_date)

def percentageudate_query(form, mode, user):
    x = ProjectAllocation.objects.get(project_id=int(mode[0]), user_id=int(mode[1]), role=mode[2])
    past = x.allocation
    update = int(mode[3])
    user.percentage = user.percentage - past
    user.percentage = user.percentage + update
    user.save()
