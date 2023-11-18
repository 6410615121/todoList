from django import forms
from task.models import Task
from .models import Project

class ProjectTaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title','TeamUser', 'Due_Date', 'description']

        widgets = {
            'Due_Date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'format': 'yyyy-MM-ddTHH:mm'}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

        # If a project is provided, filter the TeamUser choices
        if project:
            project_members = project.TeamMember.all()
            self.fields['TeamUser'].queryset = project_members

class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['Project_name',
                  'TeamMember',
                  'TeamLeader',
                  ]
        

    def __init__(self,*args, project=None, **kwargs,):
        super().__init__(*args, **kwargs)

        if project:
            project_members = project.TeamMember.all()
            self.fields['TeamMember'].queryset = project_members

        