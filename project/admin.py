from django.contrib import admin
from .models import Project #, Team 

# Register your models here.

class projectAdmin(admin.ModelAdmin):
    filter_horizontal = ("TeamMember",)
admin.site.register(Project,projectAdmin)

"""class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ("TeamMember",)
admin.site.register(Team, TeamAdmin)"""


