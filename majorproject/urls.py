from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="base.html"), name="base"),
    path('account/', include('allauth.urls')),
    path('registration/', include('registration.urls')),
    path('task/', include('task.urls')),
    path('project/', include('project.urls')),
    path('task/', include('task.urls')),
    path('charts_and_reports/', include('charts_and_reports.urls')),
]
