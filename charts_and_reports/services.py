from project.models import Project, ProjectAllocation, Teamlead
from registration.models import User
from task.models import Task, TaskAllocation
import json

def userallocatedinproject():
    if User.user_query().get('allusers').count() and Project.project_query().get(
                'allprojects').count():

        context = {
            'allocatedusers': User.objects.filter(id__in=ProjectAllocation.objects.all().values('user_id')),
            'allocatepercent': (User.objects.filter(id__in=ProjectAllocation.objects.all().values('user_id')).count() / User.user_query().get(
                'allusers').count()) * 100,
            'failpercent': (Project.objects.filter(status='closed').count() / Project.project_query().get(
                    'allprojects').count()) * 100,
            'finishpercent': (Project.objects.filter(status='created').count() / Project.project_query().get(
                    'allprojects').count()) * 100,
            'wellpercent': (Project.objects.filter(status='Underprogress').count() / Project.project_query().get(
                    'allprojects').count()) * 100
        }
    else:
        context = {
            'allocatedusers': User.objects.filter(id__in=ProjectAllocation.objects.all().values('user_id')),
            'allocatepercent': (User.objects.filter(id__in=ProjectAllocation.objects.all().values('user_id')).count() / 1) * 100,
            'failpercent': (Project.objects.filter(status='closed').count() / 1) * 100,
            'finishpercent': (Project.objects.filter(status='created').count() / 1) * 100,
            'wellpercent': (Project.objects.filter(status='Underprogress').count() / 1) * 100
        }
    return context

def allocationchart_query():
    projects = []
    allocation = []
    for project in Project.project_query().get('allprojects')[:10]:
        allocation.append(int(ProjectAllocation.objects.filter(project_id=project.id).count()))
        projects.append(project.name)
    allocation.append(User.user_query().get('allusers').count())
    context = {
        'projects': projects,
        'allocation': allocation
    }
    return context


def employeegraph_query(user):
    y = 0
    allocation = []
    projects = []
    for project in Project.objects.all():
        projects.append(project.name)
        for allocacy in ProjectAllocation.objects.filter(user_id=int(user), project_id=project.id):
            y += allocacy.allocation
        allocation.append(y)
        y = 0
    allocation.append(100)
    context = {
        'projects': projects,
        'allocation': allocation
    }
    return context

def selectedemployeegraph_query(user):
    y = 0
    allocation = []
    projects = []
    for project in Project.objects.all():
        projects.append(project.name)
        for allocacy in ProjectAllocation.objects.filter(user_id=user, project_id=project.id):
            y += allocacy.allocation
        allocation.append(y)
        y = 0
    allocation.append(100)
    data = json.dumps({"projects": projects, "allocation": allocation})
    context = {
        'data': data,
    }
    return context

# def report_query(staff, superuser, year, user):
#     print(year+"vgvgygy")
#     print(superuser)
    # print(user.is_staff)
    # print(user.is_superuser)
    # if user.is_staff or y:
    #     print('qwwq')
    # else:
    #     print('sdfsfd')