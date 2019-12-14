from django import template

register = template.Library()


@register.simple_tag
def get_task_assigines(task):
    return task.taskallocation.all()

@register.simple_tag
def get_project_assigines(project):
    return project.projectallocation_set.all()

# @register.simple_tag
# def get_project(project):
    # context = {"projects": Project.objects.all().count(), }
    # return


