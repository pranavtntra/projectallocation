from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import transaction
from .models import Project, ProjectAllocation, Teamlead
from registration.models import User
from .forms import Projectform, Assignleaderform, Allocateemployeeform, Allocateemployeebyleadform, Allocateemployeesssform
from django.views.generic import View, ListView, UpdateView, DeleteView
from task.models import Task
from .services import projectview_query, percentageudate_query
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime
import json
from django.http import JsonResponse
from django.core import serializers

project_list = Project.objects.all().order_by('id')


class ProjectList(View):

    @transaction.atomic
    def get(self, request):
        project_list_list = Project.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(project_list_list, 2)
        try:
            project_list = paginator.page(page)
        except PageNotAnInteger:
            project_list = paginator.page(1)
        except EmptyPage:
            project_list = paginator.page(paginator.num_pages)
        return render(request, 'project/projectlist.html', {'project_list': project_list, 'project_list_list': project_list_list,
                                                            "allproject": Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())})

class SearchView(View):

    def get(self, request):
        q = request.GET.get('q', None)
        project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q))
        if project_list_list:
            page = request.GET.get('page', 1)
            paginator = Paginator(project_list_list, 2)
            try:
                project_list = paginator.page(page)
            except PageNotAnInteger:
                project_list = paginator.page(1)
            except EmptyPage:
                project_list = paginator.page(paginator.num_pages)
            return render(request, 'project/projectlist.html', {'project_list': project_list, 'q': q})
        else:
            error = "No such data found."
            project_list_list = Project.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(project_list_list, 2)
            try:
                project_list = paginator.page(page)
            except PageNotAnInteger:
                project_list = paginator.page(1)
            except EmptyPage:
                project_list = paginator.page(paginator.num_pages)
            return render(request, 'project/projectlist.html', {'project_list': project_list, 'error': error})


class Projectforlead(View):

    @transaction.atomic
    def get(self, request):
        return render(request, 'project/projectlist.html', {'project_list': project_list,
                                                            "allproject": Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())})


class Projectforemployee(View):

    @transaction.atomic
    def get(self, request):
        return render(request, 'project/projectlist.html', {'project_list': project_list,
                                                            "allproject": Project.objects.filter(projectallocation__in=self.request.user.projectallocation_set.all())})


class ProjectUpdateView(UpdateView):
    template_name = 'project/projectupdate.html'
    model = Project
    success_url = reverse_lazy('projectlist')
    fields = ['name', 'description', 'status', 'start_date', 'end_date']
    context_object_name = 'form'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Project, id=id)

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return redirect("projectlist")


class ProjectDeleteView(DeleteView):
    model = Project
    context_object_name = 'form'
    success_url = reverse_lazy('projectlist')
    template_name = 'project/projectdelete.html'


class ProjectdetailView(View):

    @transaction.atomic
    def get(self, request, id):
        return render(request, 'project/project_detail.html', {'project': Project.objects.get(id=int(id)),
                                                               'dev': ProjectAllocation.objects.filter(project_id=int(id), role=1),
                                                               'lead': Teamlead.objects.filter(project_id=int(id)),
                                                               'error': 'error',
                                                               'qa': ProjectAllocation.objects.filter(project_id=int(id), role=3),
                                                               'ui': ProjectAllocation.objects.filter(project_id=int(id), role=2)})


class ProjectView(View):

    @transaction.atomic
    def get(self, request):
        form = Projectform
        return render(request, 'project/create.html', {'form': form,
                                                       'employee': User.objects.all(),
                                                       'error': 'error'})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Projectform(request.POST)
        errors = "Make sure you entered dates correctly."
        if request.POST.get('start_date') and request.POST.get('end_date') and request.POST.get(
                'start_date') < request.POST.get('end_date'):
            if Project.objects.filter(name=request.POST.get('name')).count() > 0:
                return render(request, 'project/create.html', {'form': form,
                                                               'error': 'error',
                                                               'employee': User.objects.all()})
            else:
                try:
                    project = Project.objects.latest('id')
                    project = project.id + 1
                except Exception as e:
                    project = 1
                if request.POST.get('lead'):
                    projectview_query(project, request.POST.get('lead'), request.POST.get('name'), request.POST.get('description'), request.POST.get('start_date'), request.POST.get('end_date'), request.POST.get('status'))
                form = Allocateemployeesssform
                return render(request, 'project/create.html', {'form': form,
                                                               'project': project})
        else:
            return render(request, 'project/create.html', {'form': form,
                                                           'errors': errors,
                                                           'employee': User.objects.all()})


class AssignleaderView(View):

    @transaction.atomic
    def get(self, request):
        form = Assignleaderform
        return render(request, 'project/assignleader.html', {'form': form, 'error': 'error'})

    @transaction.atomic
    def post(self, request, **kwargs):
        x = User.objects.get(id=int(request.POST.get('user')))
        x.is_staff = True
        x.save()
        if Teamlead.objects.filter(project_id=int(request.POST.get('project')), user_id=int(request.POST.get('user'))).count() == 0:
            Teamlead.objects.create(project_id=int(request.POST.get('project')), user_id=int(request.POST.get('user')))
            return redirect('userdashboard')
        else:
            form = Assignleaderform
            errors = "Employee already Team Lead in this Project."
            return render(request, 'project/assignleader.html', {'form': form, 'error': 'error', 'errors': errors})


class LeadListView(ListView):

    model = Teamlead
    template_name = "project/leadlist.html"

    def get_queryset(self):
        return Teamlead.objects.all().order_by('project_id')


class LeadUpdateView(UpdateView):
    template_name = 'project/leadupdate.html'
    model = Teamlead
    success_url = reverse_lazy('leadlist')
    fields = ['project', 'user']
    context_object_name = 'form'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Teamlead, id=id)

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return redirect("leadlist")


class LeadDeleteView(DeleteView):
    model = Teamlead
    context_object_name = 'form'
    success_url = reverse_lazy('leadlist')
    template_name = 'project/leaddelete.html'


class AllocateemployeeView(View):

    @transaction.atomic
    def get(self, request):
        form = Allocateemployeeform
        return render(request, 'project/allocateemployee.html', {'form': form})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Allocateemployeeform(request.POST)
        user = User.objects.get(id=int(request.POST.get('user')))
        percent = str(100 - user.percentage)
        errors = "Please assign other employee or make percentage value less than or equal to " + percent + '.'
        if request.POST.get('project') and request.POST.get('percentage'):
            updated_value = user.percentage + int(request.POST.get('percentage'))
            if updated_value < 101:
                User.objects.filter(id=int(request.POST.get('user'))).update(percentage=updated_value)
                ProjectAllocation.objects.create(project_id=int(request.POST.get('project')), user_id=int(request.POST.get('user')), role=request.POST.get('role'), allocation=int(request.POST.get('percentage')))
                return redirect('projectlist')
        elif form.is_valid() and request.POST.get('percentage'):
            updated_value = user.percentage + int(request.POST.get('percentage'))
            if updated_value < 101:
                User.objects.filter(id=int(request.POST.get('user'))).update(percentage=updated_value)
                ProjectAllocation.objects.create(project_id=int(request.POST.get('project')), user_id=int(request.POST.get('user')), role=request.POST.get('role'), allocation=int(request.POST.get('percentage')))
                return redirect('projectlist')
        return render(request, "project/allocateemployee.html", {'form': form, 'error': 'error', 'errors': errors})


class AllocationListView(ListView):

    model = ProjectAllocation
    template_name = "project/allocationlist.html"
    paginate_by = 4

    def get_queryset(self):
        return ProjectAllocation.objects.all().order_by('project_id')


class AllocationUpdateView(UpdateView):
    template_name = 'project/allocationupdate.html'
    model = ProjectAllocation
    success_url = reverse_lazy('allocationlist')
    fields = ['project', 'user', 'role', 'allocation']
    context_object_name = 'form'
    x = 0

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(ProjectAllocation, id=id)

    def form_valid(self, form):
        mode = []
        for i in form:
            mode.append(i.value())
        user = User.objects.get(id=int(mode[1]))
        if user.percentage + int(mode[3]) > 99:
            if user.percentage == 100:
                error = "Please select another user as this user is fully occupied."
                return render(self.request, 'project/allocationupdate.html', {'form': form, 'error': error})
            error = "Please provide allocation " + "less than " + str(100 - user.percentage) + "."
            return render(self.request, 'project/allocationupdate.html', {'form': form, 'error': error})

        else:
            percentageudate_query(form, mode, user)
            super().form_valid(form)
            form.save()
        return redirect("allocationlist")


class AllocationDeleteView(View):

    @transaction.atomic
    def get(self, request, pk, id, *args, **kwargs):
        employee = User.objects.get(id=int(pk))
        allocation = int(id)
        return render(request, "project/allocationdelete.html", {'allocation': allocation, 'employee': employee})

    @transaction.atomic
    def post(self, request, pk, id):
        x = User.objects.get(id=int(pk))
        x.percentage = x.percentage - int(id)
        x.save()
        return redirect('allocationlist')


class AllocateemployeebyleadView(View):

    @transaction.atomic
    def get(self, request):
        form = Allocateemployeebyleadform
        return render(request, 'project/allocateemployeebylead.html', {'form': form, 'project': Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())})

    @transaction.atomic
    def post(self, request, **kwargs):
        form = Allocateemployeebyleadform(request.POST)
        project = Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all())
        user = User.objects.get(id=int(request.POST.get('user')))
        percent = str(100 - user.percentage)
        errors = "Please assign other employee or make percentage value less than or equal to " + percent + '.'
        if form.is_valid() and request.POST.get('percentage'):
            updated_value = user.percentage + int(request.POST.get('percentage'))
            if updated_value < 101:
                User.objects.filter(id=int(request.POST.get('user'))).update(percentage=updated_value)
                ProjectAllocation.objects.create(project_id=int(request.POST.get('project')), user_id=int(request.POST.get('user')), role=request.POST.get('role'), allocation=int(request.POST.get('percentage')))
                return redirect('projectlist')
        return render(request, "project/allocateemployeebylead.html", {'form': form, 'error': 'error', 'errors': errors, 'project': project})


class AllocationListforleadView(ListView):

    model = ProjectAllocation
    template_name = "project/allocationlistforlead.html"

    def get_queryset(self):
        projects = []
        for i in Project.objects.filter(teamlead__in=self.request.user.teamlead_set.all()):
            projects.append(i.id)
        return ProjectAllocation.objects.filter(project_id__in=projects).order_by('project_id')


class AllocationUpdateforleadView(UpdateView):
    template_name = 'project/allocationupdateforlead.html'
    model = ProjectAllocation
    success_url = reverse_lazy('allocationlistforlead')
    fields = ['project', 'user', 'role', 'allocation']
    context_object_name = 'form'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(ProjectAllocation, id=id)

    def form_valid(self, form):
        mode = []
        for i in form:
            mode.append(i.value())
        user = User.objects.get(id=int(mode[1]))
        if user.percentage + int(mode[3]) > 99:
            if user.percentage == 100:
                error = "Please select another user as this user is fully occupied."
                return render(self.request, 'project/allocationupdate.html', {'form': form, 'error': error})
            error = "Please provide allocation " + "less than " + str(100 - user.percentage) + "."
            return render(self.request, 'project/allocationupdate.html', {'form': form, 'error': error})

        else:
            percentageudate_query(form, mode, user)
            super().form_valid(form)
            form.save()
        return redirect("allocationlistforlead")


class AllocationDeleteforleadView(View):

    @transaction.atomic
    def get(self, request, pk, id, *args, **kwargs):
        employee = User.objects.get(id=int(pk))
        allocation = int(id)
        return render(request, "project/allocationdeleteforlead.html", {'allocation': allocation, 'employee': employee})

    @transaction.atomic
    def post(self, request, pk, id):
        x = User.objects.get(id=int(pk))
        x.percentage = x.percentage - int(id)
        x.save()
        return redirect('allocationlistforlead')

class ProjecthealthView(View):

    @transaction.atomic
    def get(self, request):
        values = 0
        count = 0
        values_list = []
        count_list = []
        result = []
        project = Project.objects.all().order_by('id')
        project_list = []
        status_mapper = {"Created": 0, "Under UAT": 60, "Under QA": 80, "Approved": 90, "Merged": 100}
        for projects in project:
            for tasks in projects.task_set.all():
                if tasks:
                    values += status_mapper[tasks.get_status_display()]
                    count += 1
            if count > 0:
                values_list.append(values)
                count_list.append(count)
                result.append((values/count))
                count = 0
                values = 0
                project_list.append(projects.name)
            else:
                project_list.append(projects.name)
                result.append('No tasks assigned yet.')
        data = [{"element1": element1, "element2": element2} for element1, element2 in zip(result, project_list)]
        return render(request, 'project/projecthealth.html', {'data': data})


class SortView(View):

    def get(self, request):
        name = request.GET.get('select')
        q = request.GET.get('q')
        project_list_list = []
        if name == 'na' and q:
            project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('name')
        elif name == 'nd' and q:
            project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('-name')
        elif name == 'na':
            project_list_list = Project.objects.all().order_by('name')
        elif name == 'nd':
            project_list_list = Project.objects.all().order_by('-name')
        elif name == 'sa' and q:
            project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('start_date')
        elif name == 'sd' and q:
            project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('-start_date')
        elif name == 'sa':
            project_list_list = Project.objects.all().order_by('start_date')
        elif name == 'sd':
            project_list_list = Project.objects.all().order_by('-start_date')
        elif name == 'ea' and q:
            project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('end_date')
        elif name == 'ed' and q:
            project_list_list = Project.objects.filter(Q(name__icontains=q) | Q(status__icontains=q)).order_by('-end_date')
        elif name == 'ea':
            project_list_list = Project.objects.all().order_by('end_date')
        elif name == 'ed':
            project_list_list = Project.objects.all().order_by('-end_date')
        page = request.GET.get('page', 1)

        paginator = Paginator(project_list_list, 2)
        try:
            project_list = paginator.page(page)
        except PageNotAnInteger:
            project_list = paginator.page(1)
        except EmptyPage:
            project_list = paginator.page(paginator.num_pages)
        return render(request, 'project/projectlist.html', {'project_list': project_list, 'name': name, 'q': q})


class SearchResultView(View):

    def get(self, request):
        projectname = request.GET.get('projectname', None)
        startdate = request.GET.get('startdate', None)
        enddate = request.GET.get('enddate', None)
        status = request.GET.get('status', None)
        stat = "both"
        if projectname and startdate and enddate and status:
            project_list_list = Project.objects.filter(Q(name__icontains=projectname) & Q(status__icontains=status) & Q(start_date=datetime.strptime(startdate,'%Y-%m-%d').date()) & Q(end_date=datetime.strptime(enddate,'%Y-%m-%d').date()))
        if projectname or startdate or enddate or status:
            try:
                project_list_list = Project.objects.filter(
                    Q(name__icontains=projectname) | Q(status__icontains=status) | Q(end_date=datetime.strptime(enddate, '%Y-%m-%d').date()))
            except ValueError as e:
                stat = 'noend'
            try:
                project_list_list = Project.objects.filter(Q(name__icontains=projectname) | Q(status__icontains=status) | Q(start_date=datetime.strptime(startdate, '%Y-%m-%d').date()))
            except ValueError as e:
                stat += 'nostart'
            if stat == 'both':
                project_list_list = Project.objects.filter(
                    Q(name__icontains=projectname) | Q(status__icontains=status) | Q(end_date=datetime.strptime(enddate, '%Y-%m-%d').date()) | Q(start_date=datetime.strptime(startdate, '%Y-%m-%d').date()))
            elif stat == "noend":
                project_list_list = Project.objects.filter(
                    Q(name__icontains=projectname) | Q(status__icontains=status) | Q(start_date=datetime.strptime(startdate, '%Y-%m-%d').date()))
            elif stat == 'nostart':
                project_list_list = Project.objects.filter(
                    Q(name__icontains=projectname) | Q(status__icontains=status) | Q(end_date=datetime.strptime(enddate, '%Y-%m-%d').date()))
            elif not status:
                project_list_list = Project.objects.filter(name__icontains=projectname)
            else:
                project_list_list = Project.objects.filter(status__icontains=status)
            if not project_list_list:
                error = "No such data found."
                project_list_list = Project.objects.all()
                page = request.GET.get('page', 1)

                paginator = Paginator(project_list_list, 2)
                try:
                    project_list = paginator.page(page)
                except PageNotAnInteger:
                    project_list = paginator.page(1)
                except EmptyPage:
                    project_list = paginator.page(paginator.num_pages)
                return render(request, 'project/projectlist.html', {'project_list': project_list, 'error': error})
        page = request.GET.get('page', 1)

        paginator = Paginator(project_list_list, 2)
        try:
            project_list = paginator.page(page)
        except PageNotAnInteger:
            project_list = paginator.page(1)
        except EmptyPage:
            project_list = paginator.page(paginator.num_pages)
        return render(request, 'project/projectlist.html',
                      {'project_list': project_list, 'startdate': startdate, 'enddate': enddate, 'status': status,
                       'projectname': projectname})
