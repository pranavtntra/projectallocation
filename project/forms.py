from django import forms
from django.forms import ModelForm
from .models import Project, ProjectAllocation, Teamlead


class Projectform(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']


class Assignleaderform(ModelForm):
    class Meta:
        model = Teamlead
        fields = ['project', 'user']
        labels = {
            "project": "Please select Project",
            "user": "Please select Employee"
        }


class Allocateemployeeform(ModelForm):
    class Meta:
        model = ProjectAllocation
        fields = ['project', 'user', 'role']
        labels = {
            "project": "Please select Project",
            "user": "Please select Employee",
            "role": "Please select usertype"
        }


class Allocateemployeesssform(ModelForm):
    class Meta:
        model = ProjectAllocation
        fields = ['user', 'role']
        labels = {
            "user": "Please select Employee",
            "role": "Please select usertype"
        }


class Allocateemployeebyleadform(ModelForm):
    class Meta:
        model = ProjectAllocation
        fields = ['user', 'role']
        labels = {
            "user": "Please select Employee",
            "role": "Please select usertype"
        }