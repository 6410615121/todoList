from django import forms
from task.models import Task

class IndividualTaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'Due_Date', 'description']

        widgets = {
            'Due_Date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'format': 'yyyy-MM-ddTHH:mm'}),
        }

    