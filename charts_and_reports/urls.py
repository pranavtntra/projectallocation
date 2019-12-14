from django.urls import path
from .views import DashboardView, Employeelist, ReportView, AllocationchartView, EmployeegraphView, SelectedemployeegraphView


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="userdashboard"),
    path('allocationchart/', AllocationchartView.as_view(), name="allocationchart"),
    path('byemployee/', Employeelist.as_view(), name="byemployee"),
    path('employeegraph/', EmployeegraphView.as_view(), name="employeegraph"),
    path('report/', ReportView.as_view(), name="generatereport"),
    path('usergraph/', SelectedemployeegraphView.as_view(), name="selectedbyemployee"),

]