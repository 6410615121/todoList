from .models import Task , Individual_Task
from django import forms





class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['Project', 'Teamleader', 'TeamUser', 'task_title', 'Due_Date','Finish_Date', 'description']
    
    
    
    '''
    TeamUser = forms.ModelMultipleChoiceField(
        queryset=Friend.objects.all(),

        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    '''
   

class IndividualTaskForm(forms.ModelForm):
    
    class Meta:
        model = Individual_Task
        fields = ['User', 'task_title', 'Due_Date', 'Finish_Date','description']

        
    