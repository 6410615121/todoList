from django import forms
from .models import Project
from user.models import todoUser

class CreateprojectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['Project_name', 'TeamUser']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove 'user' from kwargs
        super(CreateprojectForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filter the queryset for the TeamUser field to include only friends of the current user
            tdu = todoUser.objects.get(user=user)
            self.fields['TeamUser'].queryset = tdu.friends.all()