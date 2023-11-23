from django import forms
from task.models import Task

class IndividualTaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'Due_Date', 'description']

        widgets = {
            'Due_Date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        input_formats = {
            'Due_Date': ['%Y-%m-%dT%H:%M'],
        }
