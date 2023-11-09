from django.contrib import admin
from .models import Project

# Register your models here.
class projectAdmin(admin.ModelAdmin):
    filter_horizontal = ("TeamMember",)
admin.site.register(Project,projectAdmin)
