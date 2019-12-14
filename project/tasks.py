from celery.task.schedules import crontab
from celery.decorators import periodic_task,task
from django.utils import timezone
from task.models import Task

@task(name='test_task')
def test():
    print("00000000000000000000000000000")

@periodic_task(run_every=(crontab(minute="30", hour="16")), name="deadline_task", ignore_result=True)
def deadline_test():
    date = timezone.now().date()
    print(date)
    tasks = Task.objects.all()
    projects = []
    for task in tasks:
        if task.deadline < date and task.project.name not in projects:
            projects.append(task.project.name)
    return projects

