from django.contrib import admin
from .models import Project, ProjectAllocation, Teamlead

admin.site.register(Project)
admin.site.register(ProjectAllocation)
admin.site.register(Teamlead)

admin.site.site_header = 'Admin Project Allocation Dashboard'

class ProjectAdmin(admin.ModelAdmin):
    pass
