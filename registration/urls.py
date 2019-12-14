from django.urls import path, include
from .views import UserView, UserList, UserUpdateView, UserDeleteView, EmployeeSearchView
from registration import views

urlpatterns = [
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('addemployee/', UserView.as_view(), name='signingup'),
    path('list/', UserList.as_view(), name="employeelist"),
    path('userupdate/<int:id>', UserUpdateView.as_view(), name="update"),
    path('userdelete/<int:pk>', UserDeleteView.as_view(), name="delete"),
    path('employeesearch/', EmployeeSearchView.as_view(), name='employeesearch'),
]