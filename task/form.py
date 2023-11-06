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
        fields = ['Project_ID', 'Teamleader_ID', 'TeamUser_ID', 'task_title', 'Due_Date','Finish_Date', 'description']

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
    