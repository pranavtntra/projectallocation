from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from task import views
from .views import TaskView, TaskbyleadView, SubtaskView, SubtaskbyleadView, AllocateemployeeView, AllocateemployeebyleadView, validate_task, SubtaskbydeveloperView, TaskList, TaskUpdateView, TaskDeleteView, TaskforleadList, TaskbyuserView, TaskdetailView, TaskSearchView, SearchforleadView, SearchforemployeeView, SortView, SortViewforlead

urlpatterns = [
    path('tasklist/', TaskList.as_view(), name="tasklist"),
    path('tasklistforlead/', TaskforleadList.as_view(), name="tasklistforlead"),
    path('createtask/', TaskView.as_view(), name='createtask'),
    path('taskbylead/', TaskbyleadView.as_view(), name='taskbylead'),
    path('taskbyuser/', TaskbyuserView.as_view(), name='tasklistforusers'),
    path('createsubtask/', SubtaskView.as_view(), name='createsubtask'),
    path('subtaskbylead/', SubtaskbyleadView.as_view(), name='subtaskbylead'),
    path('subtaskbydeveloper/', SubtaskbydeveloperView.as_view(), name='subtaskbydeveloper'),
    path('allocation/', AllocateemployeeView.as_view(), name='allocateemployee_task'),
    path('allocationbylead/', AllocateemployeebyleadView.as_view(), name='allocateemployee_task_lead'),
    path('ajaxjson/', views.validate_task, name='validate_task'),
    path('taskupdate/<int:id>', TaskUpdateView.as_view(), name="taskupdate"),
    path('taskdelete/<int:pk>', TaskDeleteView.as_view(), name="taskdelete"),
    path('taskdetail/<int:id>', TaskdetailView.as_view(), name="taskdetail"),
    path('search/', TaskSearchView.as_view(), name='tasksearch'),
    path('leadsearch/', SearchforleadView.as_view(), name='leadtasksearch'),
    path('employeesearch/', SearchforemployeeView.as_view(), name='employeetasksearch'),
    path('tasksort/', SortView.as_view(), name='tasksort'),
    path('tasksortlead/', SortViewforlead.as_view(), name='tasksortforlead'),
]