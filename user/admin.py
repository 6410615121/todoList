from django.contrib import admin
from .models import todoUser ,Friend_request
# Register your models here.
class todoUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends',)  # This allows for a user-friendly way to select friends via a multi-select box
admin.site.register(todoUser, todoUserAdmin)
admin.site.register(Friend_request)