from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.db import transaction
from django.utils import timezone
from registration.models import User
from project.models import Teamlead, Project, ProjectAllocation
from .models import Task, TaskAllocation
from .forms import Taskform, Taskbyleadform, Subtaskform, Subtaskbyleadform, Allocateemployeeform, Allocateemployeebyleadform, Subtaskbydeveloperform
from django.core import serializers
from django.http import JsonResponse
from django.views.generic import View, ListView, UpdateView, DeleteView
import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class TaskList(ListView):
    model = Task
    template_name = 'task/tasklist.html'
    context_object_name = 'task_list'
    paginate_by = 4

    def get_queryset(self):
        return Task.objects.all().order_by('project_id')


class TaskSearchView(View):

    def get(self, request):
        q = request.GET.get('q', None)
        task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q))
        if task_list_list:
            page = request.GET.get('page', 1)
            paginator = Paginator(task_list_list, 4)
            try:
                task_list = paginator.page(page)
            except PageNotAnInteger:
                task_list = paginator.page(1)
            except EmptyPage:
                task_list = paginator.page(paginator.num_pages)
            return render(request, 'task/tasklist.html', {'task_list': task_list, 'q': q})
        else:
            error = "No such data found."
            task_list_list = Task.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(task_list_list, 4)
            try:
                task_list = paginator.page(page)
            except PageNotAnInteger:
                task_list = paginator.page(1)
            except EmptyPage:
                task_list = paginator.page(paginator.num_pages)
            return render(request, 'task/tasklist.html', {'task_list': task_list, 'error': error})


class TaskforleadList(ListView):
    model = Task
    template_name = 'task/tasklist.html'
    context_object_name = 'task_list'
    paginate_by = 4

    def get_queryset(self):
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        return Task.objects.filter(project__in=project).order_by('project_id')


class SearchforleadView(View):

    def get(self, request):
        q = request.GET.get('q', None)
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project))
        if task_list_list:
            page = request.GET.get('page', 1)
            paginator = Paginator(task_list_list, 4)
            try:
                task_list = paginator.page(page)
            except PageNotAnInteger:
                task_list = paginator.page(1)
            except EmptyPage:
                task_list = paginator.page(paginator.num_pages)
            return render(request, 'task/tasklist.html', {'task_list': task_list, 'q': q})
        else:
            error = "No such data found."
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(project__in=project).order_by('project_id')
            page = request.GET.get('page', 1)

            paginator = Paginator(task_list_list, 4)
            try:
                task_list = paginator.page(page)
            except PageNotAnInteger:
                task_list = paginator.page(1)
            except EmptyPage:
                task_list = paginator.page(paginator.num_pages)
            return render(request, 'task/tasklist.html', {'task_list': task_list, 'error': error})


class SearchforemployeeView(View):

    def get(self, request):
        q = request.GET.get('q', None)
        projectlist = []
        for p in Task.objects.filter(taskallocation__in=self.request.user.taskallocation_set.all()):
            projectlist.append(p.project.id)
        task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=projectlist))
        if task_list_list:
            page = request.GET.get('page', 1)
            paginator = Paginator(task_list_list, 4)
            try:
                task_list = paginator.page(page)
            except PageNotAnInteger:
                task_list = paginator.page(1)
            except EmptyPage:
                task_list = paginator.page(paginator.num_pages)
            return render(request, 'task/tasklist.html', {'task_list': task_list, 'q': q})
        else:
            error = "No such data found."
            page = request.GET.get('page', 1)

            paginator = Paginator(task_list_list, 4)
            try:
                task_list = paginator.page(page)
            except PageNotAnInteger:
                task_list = paginator.page(1)
            except EmptyPage:
                task_list = paginator.page(paginator.num_pages)
            return render(request, 'task/tasklist.html', {'task_list': Task.objects.filter(taskallocation__in=self.request.user.taskallocation_set.all()).order_by('project_id'), 'error': error})


class TaskbyuserView(ListView):
    model = Task
    template_name = 'task/tasklist.html'
    context_object_name = 'task_list'
    paginate_by = 4

    def get_queryset(self):
        return Task.objects.filter(taskallocation__in=self.request.user.taskallocation_set.all()).order_by('project_id')



class TaskUpdateView(UpdateView):
    template_name = 'task/taskupdate.html'
    model = Task
    success_url = reverse_lazy('tasklist')
    fields = ['project', 'name', 'description', 'status']
    context_object_name = 'form'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Task, id=id)

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        if self.request.user.is_superuser:
            return redirect("tasklist")
        else:
            return redirect("tasklistforlead")


class TaskDeleteView(DeleteView):
    model = Task
    context_object_name = 'form'
    success_url = reverse_lazy('tasklist')
    template_name = 'task/taskdelete.html'


class TaskdetailView(View):

    @transaction.atomic
    def get(self, request, id):
        task = Task.objects.get(id=int(id))
        dev = TaskAllocation.objects.filter(task_id=int(id), role=1)
        ui = TaskAllocation.objects.filter(task_id=int(id), role=2)
        qa = TaskAllocation.objects.filter(task_id=int(id), role=3)
        return render(request, 'task/task_detail.html', {'task': task, 'dev': dev, 'error': 'error', 'qa': qa, 'ui': ui})


class TaskView(View):
    @transaction.atomic
    def get(self, request):
        form = Taskform
        return render(request, 'task/create.html', {'form': form, 'error': 'error'})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Taskform(request.POST)
        errors = "Please provide proper deadline."
        description = request.POST.get('description') + "\n" + "Created by Admin"
        if request.POST.get('deadline') and str(timezone.now().date()) <= str(request.POST.get('deadline')):
            Task.objects.create(project_id=request.POST.get('project'), name=request.POST.get('name'), description=description, deadline=request.POST.get('deadline'), status=request.POST.get('status'))
            return redirect('tasklist')
        return render(request, 'task/create.html', {'form': form, 'errors': errors})


class TaskbyleadView(View):

    @transaction.atomic
    def get(self, request):
        form = Taskbyleadform
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        return render(request, 'task/taskbylead.html', {'form': form, 'project': project})

    @transaction.atomic
    def post(self, request):
        form = Taskbyleadform(request.POST)
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        errors = "Please provide proper deadline."
        description = request.POST.get('description') + "\n" + "Created by Project lead"
        if request.POST.get('deadline') and str(timezone.now().date()) <= str(request.POST.get('deadline')):
            Task.objects.create(project_id=request.POST.get('project'), name=request.POST.get('name'),
                                description=description, deadline=request.POST.get('deadline'), status=request.POST.get('status'))
            return redirect('tasklist')
        return render(request, 'task/taskbylead.html', {'form': form, 'errors': errors, 'project': project})


class SubtaskView(View):

    @transaction.atomic
    def get(self, request):
        form = Subtaskform
        project = Project.objects.all()
        return render(request, 'task/subtask.html', {'form': form, 'project': project})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Subtaskform(request.POST)
        project = Project.objects.all()
        errors = "Please provide proper deadline."
        error = "Please provide parent task or else create a task."
        description = request.POST.get('description') + "\n" + "Created by Admin"
        if request.POST.get('deadline') and str(timezone.now().date()) <= str(request.POST.get('deadline')):
            if request.POST.get('task'):
                Task.objects.create(project_id=request.POST.get('project'), name=request.POST.get('name'), description=description, deadline=request.POST.get('deadline'), parent_id=request.POST.get('task'), status=request.POST.get('status'))
                return redirect('tasklist')
            else:
                return render(request, 'task/subtask.html', {'form': form, 'error': error, 'project': project})
        else:
            return render(request, 'task/subtask.html', {'form': form, 'errors': errors, 'project': project})


class SubtaskbyleadView(View):

    @transaction.atomic
    def get(self, request):
        form = Subtaskbyleadform
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        # parent = Task.objects.filter(project__teamlead__in=self.request.user.teamlead_set.all())
        return render(request, 'task/subtaskbylead.html', {'form': form, 'project': project})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Subtaskbyleadform(request.POST)
        errors = "Please provide proper deadline."
        error = "Please provide parent task or else create a task."
        description = request.POST.get('description') + "\n" + "Created by Team Lead"
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        project_task = Task.objects.get(id=int(request.POST.get('task')))
        if request.POST.get('deadline') and str(timezone.now().date()) <= str(request.POST.get('deadline')):
            if request.POST.get('task'):
                Task.objects.create(project_id=project_task.project.id, name=request.POST.get('name'), description=description, deadline=request.POST.get('deadline'), parent_id=int(request.POST.get('task')), status=request.POST.get('status'))
                return redirect('tasklist')
            else:
                return render(request, 'task/subtaskbylead.html', {'form': form, 'error': error, 'project': project})
        else:
            return render(request, 'task/subtaskbylead.html', {'form': form, 'errors': errors, 'project': project})


class SubtaskbydeveloperView(View):
    @transaction.atomic
    def get(self, request):
        form = Subtaskbydeveloperform
        task = Task.objects.filter(taskallocation__in=self.request.user.taskallocation_set.all())
        projects = ProjectAllocation.objects.filter(user_id=self.request.user.id).distinct('project_id')
        print(projects)
        error = "You are not allocated in any tasks."
        if not task:
            return render(request, 'task/subtaskbydeveloper.html', {'error': error})
        return render(request, 'task/subtaskbydeveloper.html', {'form': form, 'task': task, 'projects': projects})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Subtaskbydeveloperform(request.POST)
        task = Task.objects.filter(taskallocation__in=self.request.user.taskallocation_set.all())
        error = "You are not allocated in any tasks."
        errors = "Please provide proper deadline."
        description = request.POST.get('description') + "\n" + "Created by Developer"
        project_task = Task.objects.get(id=int(request.POST.get('task')))
        if request.POST.get('deadline') and str(timezone.now().date()) <= str(request.POST.get('deadline')):
            if request.POST.get('task'):
                Task.objects.create(project_id=project_task.project.id, name=request.POST.get('name'), description=description, deadline=request.POST.get('deadline'), parent_id=int(request.POST.get('task')), status=request.POST.get('status'))
                return redirect('tasklist')
            else:
                return render(request, 'task/subtaskbydeveloper.html', {'form': form, 'task': task, 'error': error})
        else:
            return render(request, 'task/subtaskbydeveloper.html', {'form': form, 'task': task, 'errors': errors})


class AllocateemployeeView(View):

    @transaction.atomic
    def get(self, request):
        form = Allocateemployeeform
        y = []
        for i in Task.objects.all():
            y.append(i.project.id)
        project = Project.objects.filter(id__in=y)
        return render(request, 'task/allocateemployee.html', {'form': form, 'project': project})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Allocateemployeeform(request.POST)
        y = []
        for i in Task.objects.all():
            y.append(i.project.id)
        project = Project.objects.filter(id__in=y)
        if not request.POST.get('employee'):
            errors = "Please assign any employee to the project and then assign task."
            return render(request, "task/allocateemployee.html",
                          {'form': form, 'error': 'error', 'errors': errors, 'project': project})
        user = User.objects.get(id=int(request.POST.get('employee')))
        print(user)
        print(request.POST.get('employee'))
        percent = str(100 - user.percentage)
        errors = "Please assign other employee or make percentage value less than or equal to " + percent + '.'
        if request.POST.get('percentage'):
            updated_value = user.percentage + int(request.POST.get('percentage'))
            if form.is_valid() and updated_value < 101:
                User.objects.filter(id=int(request.POST.get('employee'))).update(percentage=updated_value)
                TaskAllocation.objects.create(task_id=request.POST.get('task'), user_id=request.POST.get('employee'), role=request.POST.get('role'), allocation=int(request.POST.get('percentage')))
                return redirect('tasklist')
        return render(request, "task/allocateemployee.html", {'form': form, 'error': 'error', 'errors': errors, 'project': project})


class AllocateemployeebyleadView(View):

    @transaction.atomic
    def get(self, request):
        form = Allocateemployeebyleadform
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        return render(request, 'task/allocateemployeebylead.html', {'form': form, 'project': project})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Allocateemployeebyleadform(request.POST)
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        user = User.objects.get(id=int(request.POST.get('user')))
        updated_value = user.percentage + int(request.POST.get('percentage'))
        percent = str(100 - user.percentage)
        if updated_value > 101:
            errors = "Please assign other employee or make percentage value less than or equal to " + percent + '.'
            return render(request, 'task/allocateemployeebylead.html', {'form': form, 'errors': errors, 'project': project})
        else:
            TaskAllocation.objects.create(task_id=int(request.POST.get('task')), user_id=int(request.POST.get('user')), role=request.POST.get('role'))
            User.objects.filter(id=int(request.POST.get('user'))).update(percentage=updated_value)
            return redirect('userdashboard')


def validate_task(request):
    project = request.GET.get('project', None)
    x = ProjectAllocation.objects.filter(project_id=int(project))
    employee = []
    for u in x:
        employee.append(u.user.username)
    tasks = serializers.serialize('json', Task.objects.filter(project_id=int(project), parent=None), fields=('name'))
    employee = ProjectAllocation.objects.filter(project_id=int(project)).values('user__username', 'user', 'user__percentage').distinct('user__username')
    print(employee)
    employee = json.dumps(list(employee))
    data = {"task": tasks, 'employee': employee}
    return JsonResponse(data, safe=False)

class SortView(View):

    def get(self, request):
        name = request.GET.get('select')
        q = request.GET.get('q')
        task_list_list = []
        if name == 'na' and q:
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('name')
        elif name == 'nd' and q:
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('-name')
        elif name == 'na':
            task_list_list = Task.objects.all().order_by('name')
        elif name == 'nd':
            task_list_list = Task.objects.all().order_by('-name')
        elif name == 'da' and q:
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('deadline')
        elif name == 'dd' and q:
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('-deadline')
        elif name == 'da':
            task_list_list = Task.objects.all().order_by('deadline')
        elif name == 'dd':
            task_list_list = Task.objects.all().order_by('-deadline')
        page = request.GET.get('page', 1)

        paginator = Paginator(task_list_list, 4)
        try:
            task_list = paginator.page(page)
        except PageNotAnInteger:
            task_list = paginator.page(1)
        except EmptyPage:
            task_list = paginator.page(paginator.num_pages)
        return render(request, 'task/tasklist.html', {'task_list': task_list, 'name': name, 'q': q})


class SortViewforlead(View):

    def get(self, request):
        name = request.GET.get('select')
        q = request.GET.get('q')
        task_list_list = []
        if name == 'na' and q:
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('name')
        elif name == 'nd' and q:
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('-name')
        elif name == 'na':
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('name')
        elif name == 'nd':
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('-name')
        elif name == 'da' and q:
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('deadline')
        elif name == 'dd' and q:
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('-deadline')
        elif name == 'da':
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('deadline')
        elif name == 'dd':
            project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
            task_list_list = Task.objects.filter(Q(name__icontains=q) | Q(status__icontains=q), Q(project__in=project)).order_by('-deadline')
        page = request.GET.get('page', 1)

        paginator = Paginator(task_list_list, 4)
        try:
            task_list = paginator.page(page)
        except PageNotAnInteger:
            task_list = paginator.page(1)
        except EmptyPage:
            task_list = paginator.page(paginator.num_pages)
        return render(request, 'task/tasklist.html', {'task_list': task_list, 'name': name, 'q': q})
