from django.contrib import admin
from .models import todoUser ,Friend_request ,Forget_pass
# Register your models here.



class todoUserAdmin(admin.ModelAdmin):
    list_display = ['Firstname', 'Lastname','todoUser_ID']
    filter_horizontal = ("friends",)

admin.site.register(todoUser,todoUserAdmin)

admin.site.register(Friend_request)
admin.site.register(Forget_pass)