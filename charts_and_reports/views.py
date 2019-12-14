from django.shortcuts import render, HttpResponse
from django.db import transaction
from project.models import Project, ProjectAllocation, Teamlead
from registration.models import User
from django.views.generic import View
from django.http import JsonResponse
import os, random, xlsxwriter, json
from .services import userallocatedinproject as employeesallocated
from .services import allocationchart_query as chartquery
from .services import employeegraph_query as employeechart
from .services import selectedemployeegraph_query as selecetedemployeechart
# from .services import report_query as reportquery


class DashboardView(View):

    @transaction.atomic
    def get(self, request):
        context = {
            'totalprojects': Project.project_query().get('allprojects').count(),
            'totalusers': User.user_query().get('allusers').count(),
            'allocatepercent': employeesallocated().get('allocatepercent'),
            'allocatedusers': User.user_query().get('allusers').count(),
            'failpercent': employeesallocated().get('failpercent'),
            'finishpercent': employeesallocated().get('finishpercent'),
            'wellpercent': employeesallocated().get('wellpercent')
        }
        return render(request, 'dashboard.html', context)


class AllocationchartView(View):

    @transaction.atomic
    def get(self, request):
        data = {"projects": chartquery().get('projects'), "allocation": chartquery().get('allocation')}
        return JsonResponse(data, safe=False)


class Employeelist(View):

    @transaction.atomic
    def get(self, request):
        employee = {'employee': User.user_query().get('allusers')}
        return render(request, 'dashboard.html', employee)


class EmployeegraphView(View):

    @transaction.atomic
    def get(self, request):
        employeechart(request.GET.get('user', None))
        data = {"projects": employeechart(request.GET.get('user', None)).get('projects'),
                "allocation": employeechart(request.GET.get('user', None)).get('allocation')}
        return JsonResponse(data, safe=False)


class SelectedemployeegraphView(View):

    @transaction.atomic
    def get(self, request):
        selecetedemployeechart(request.user.id)
        data = {'data': selecetedemployeechart(request.user.id).get('data')}
        return render(request, "graph/selectedemployeegraph.html", data)


class ReportView(View):

    @transaction.atomic
    def get(self, request):
        return render(request, 'registration/emplyoeereport.html', {'employee': User.objects.all()})

    @transaction.atomic
    def post(self, request):
        # reportquery(self.request.user.is_staff, self.request.user.is_superuser, request.POST.get('year'), request.POST.get('user'))
        if self.request.user.is_staff or self.request.user.is_superuser:
            year = request.POST.get('year')
            if not year:
                error = "Please provide proper year."
                return render(request, 'registration/emplyoeereport.html', {'employee': User.objects.all(), "error": error})
            user = User.objects.get(id=int(request.POST.get('user')))
            username = user.username
            user = int(request.POST.get('user'))
        else:
            year = request.POST.get('year')
            if not year:
                error = "Please provide proper year."
                return render(request, 'registration/emplyoeereport.html', {'employee': User.objects.all(), "error": error})
            print(year)
            print(type(year))
            x = User.objects.get(id=self.request.user.id)
            username = x.username
            user = self.request.user.id
        project_list = []
        allocation_list = []
        month_list = []
        role_list = []
        data = ['Month', 'Project', 'Percent Allocation', 'Role for Project']
        value = random.randint(0, 1000)
        workbook = xlsxwriter.Workbook(username + str(value) + 'report.xlsx')
        worksheet = workbook.add_worksheet()
        file_name = username + str(value) + 'report.xlsx'
        path_url = 'C:/Users/Dell/Desktop/intership/majorproject/'
        cell_format = workbook.add_format()
        cell_format.set_bold()
        row = 0
        col = 0
        for tr in (data):
            worksheet.write(row, col, tr, cell_format)
            col += 1
        x = ProjectAllocation.objects.filter(user_id=user)
        month = {"01": "jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                 "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
        for a in x:
            print(a.project.start_date.year)
            if a.project.start_date.year == int(year):
                role_list.append(a.get_role_display())
                allocation_list.append(a.allocation)
                num = str(a.project.start_date.month)
                if num in month:
                    month_list.append(month[num])
                    project_list.append(a.project.name)
        row = 1
        for month in month_list:
            worksheet.write(row, 0, month)
            row += 1
        row = 1
        for project in project_list:
            worksheet.write(row, 1, project)
            row += 1
        row = 1
        for allocation in allocation_list:
            worksheet.write(row, 2, allocation)
            row += 1
        row = 1
        for role in role_list:
            worksheet.write(row, 3, role)
            row += 1
        workbook.close()
        path = path_url + file_name
        if 'download' in request.POST:
            if os.path.exists(path):
                with open(path, 'rb') as excel:
                    data = excel.read()

                response = HttpResponse(data,
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename= %s' % file_name
                return response
        elif 'view' in request.POST:
            data = [{"element1": element1, "element2": element2, "element3": element3, "element4": element4} for element1, element2, element3, element4 in zip(month_list, project_list, allocation_list, role_list)]
            if data:
                return render(request, 'registration/emplyoeereport.html', {'project_list': project_list, 'month_list': month_list, 'employee': User.objects.all(), "data": data})
            else:
                error = "No data found."
                return render(request, 'registration/emplyoeereport.html',
                              {'project_list': project_list, 'month_list': month_list, 'employee': User.objects.all(),
                               "data": data, "error": error})