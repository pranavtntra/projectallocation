from django import forms
from django.forms import ModelForm
from .models import Task, TaskAllocation


class Taskform(ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'name', 'description', 'status']


class Taskbyleadform(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status']


class Subtaskform(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status']
        labels = {
            "parent": "Please select Task",
}


class Subtaskbyleadform(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status']


class Subtaskbydeveloperform(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status']


class Allocateemployeeform(ModelForm):
    class Meta:
        model = TaskAllocation
        fields = ['role']
        labels = {
            "role": "Please select usertype"
        }


class Allocateemployeebyleadform(ModelForm):
    class Meta:
        model = TaskAllocation
        fields = ['user', 'role']
        labels = {
            "user": "Please select Employee",
            "role": "Please select usertype"
        }