from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import ProjectView, AssignleaderView, AllocateemployeeView, AllocateemployeebyleadView, ProjectList, ProjectUpdateView, ProjectDeleteView, Projectforlead, ProjectdetailView, LeadListView, LeadUpdateView, LeadDeleteView, AllocationListView, AllocationDeleteView, AllocationUpdateView, AllocationListforleadView, AllocationDeleteforleadView, AllocationUpdateforleadView, Projectforemployee, ProjecthealthView, SearchView, SortView, SearchResultView
from project import views

urlpatterns = [
    path('projectlist/', ProjectList.as_view(), name="projectlist"),
    path('projectlistforlead/', Projectforlead.as_view(), name="projectlistforlead"),
    path('projectlistforemployee/', Projectforemployee.as_view(), name="projectlistforemployee"),
    path('createproject/', ProjectView.as_view(), name='createproject'),
    path('projectdetail/<int:id>', ProjectdetailView.as_view(), name="projectdetail"),
    path('projectupdate/<int:id>', ProjectUpdateView.as_view(), name="projectupdate"),
    path('projectdelete/<int:pk>', ProjectDeleteView.as_view(), name="projectdelete"),
    path('assignleader/', AssignleaderView.as_view(), name='assignleader'),
    path('allocateemployee/', AllocateemployeeView.as_view(), name='allocateemployee'),
    path('allocateemployeebylead/', AllocateemployeebyleadView.as_view(), name='allocateemployeebylead'),
    path('teamlead/', LeadListView.as_view(), name='leadlist'),
    path('leadupdate/<int:id>', LeadUpdateView.as_view(), name="leadupdate"),
    path('leaddelete/<int:pk>', LeadDeleteView.as_view(), name="leaddelete"),
    path('allocationlist/', AllocationListView.as_view(), name='allocationlist'),
    path('allocationupdate/<int:id>', AllocationUpdateView.as_view(), name="allocationupdate"),
    path('allocationdelete/<int:pk>/<int:id>', AllocationDeleteView.as_view(), name="allocationdelete"),
    path('allocationlistforlead/', AllocationListforleadView.as_view(), name='allocationlistforlead'),
    path('allocationupdateforlead/<int:id>', AllocationUpdateforleadView.as_view(), name="allocationupdateforlead"),
    path('allocationdeleteforlead/<int:pk>/<int:id>', AllocationDeleteforleadView.as_view(), name="allocationdeleteforlead"),
    path('projecthealth/', ProjecthealthView.as_view(), name='projecthealth'),
    path('search/', SearchView.as_view(), name='search'),
    path('searchresult/', SearchResultView.as_view(), name='searchresult'),
    path('sort/', SortView.as_view(), name='sort'),
]