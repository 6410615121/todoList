"""from .models import Task , Individual_Task
from django import forms



class TaskForm(forms.ModelForm):
    date_range = forms.ChoiceField(
        choices=[
            ('daily', 'Daily'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        widget=forms.RadioSelect,
    )
    class Meta:
        model = Task
        fields = ['Project', 'TaskOwner', 'Task_ID', 'task_title', 'Entry_Date','Due_Date', 'Finish_Date','description']

class IndividualTaskForm(forms.ModelForm):
    date_range = forms.ChoiceField(
        choices=[
            ('daily', 'Daily'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        widget=forms.RadioSelect,
    )
    class Meta:
        model = Individual_Task
        fields = ['User_ID', 'task_title', 'Due_Date', 'Finish_Date','description']
        """
    
from django import forms
from .models import Task, Project, todoUser

class TaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # Retrieve the todoUser instance based on the User object
        todo_user_instance = todoUser.objects.get(user=user)

        # Filter the Project field based on the user's projects
        user_projects = Project.objects.filter(TeamLeader=todo_user_instance)
        self.fields['Project'].queryset = user_projects

        # Filter the TaskOwner field based on the selected project's members
        selected_project = None
        if 'Project' in self.data:
            selected_project = int(self.data.get('Project'))
        elif self.instance.pk:
            selected_project = self.instance.Project.pk if self.instance.Project else None
        
        if selected_project:
            project_members = Project.objects.get(pk=selected_project).TeamMember.all()
            self.fields['TaskOwner'].queryset = project_members

    class Meta:
        model = Task
        fields = ['Project', 'TaskOwner', 'task_title', 'Due_Date', 'description']
        widgets = {
            'Due_Date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
