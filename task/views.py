from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from .form import TaskForm
from user.models import todoUser
from project.models import Project
from .models import Individual_Task ,Task
from django.utils import timezone
# Create your views here.


def updatetask(request ,cat):
    user_profile = request.user
    mytodouser = todoUser.objects.get(user=user_profile)
    mytask = Individual_Task.objects.filter(User=mytodouser)
    for task in mytask:
        if task.Due_Date < timezone.now():
            task.category = 'pastdue'

        if task.achieve :
            task.category = 'complete'   
        task.save()
    if cat == "due":
        mytask = Individual_Task.objects.filter(User=mytodouser, category='due')
    elif cat == "past":
        mytask = Individual_Task.objects.filter(User=mytodouser, category='pastdue')
    elif cat == "com":
        mytask = Individual_Task.objects.filter(User=mytodouser, category='complete')
    print(mytask)
    return   mytask


@login_required
def individual_tasklist(request):
    mytask = updatetask(request,"due")      

        
    context = {'tasklist': mytask}
    
    return render(request, 'task/task.html',context)

@login_required
def individual_past_tasklist(request):
    mytask = updatetask(request,"past")      

        
    context = {'tasklist': mytask}
    
    return render(request, 'task/pastduetask.html',context)

@login_required
def individual_com_tasklist(request):
    mytask = updatetask(request,"com")      

        
    context = {'tasklist': mytask}
    
    return render(request, 'task/completetask.html',context)


@login_required
def individual_taskAdd(request):
    if request.method == 'POST':
        todouser = todoUser.objects.get(user = request.user)

        task_title = request.POST.get('task_title')
        Due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        Individual_Task.objects.create(User = todouser, task_title = task_title, Due_Date = Due_date, description = description)
        
        return individual_tasklist(request)

    return render(request, 'task/individual_taskAdd.html')



@login_required
def task_add(request):
    todouser = todoUser.objects.get(user = request.user)
    project_members = None
    project_selected_ID = request.session.get('project_selected', 0)
    if project_selected_ID != 0:
        selected_project = Project.objects.get(Project_ID = project_selected_ID)
    else:
        selected_project = None
    if request.method == 'POST':
        if 'submit_project' in request.POST:
            selected_project = request.POST.get('project')
            if selected_project is not None:
                request.session['project_selected'] = selected_project
                selected_project = Project.objects.get(Project_ID = selected_project)
                project_members = selected_project.TeamMember.all()

        if 'submit_task' in request.POST:
            selected_Owner = request.POST.get('task_owner')
            selected_Owner = todoUser.objects.get(todoUser_ID = selected_Owner)
            task_title = request.POST.get('task_title')
            due_date = request.POST.get('due_date')
            description = request.POST.get('description')
            Task.objects.create(Project = selected_project, TaskOwner = selected_Owner, task_title = task_title, Due_Date = due_date, description = description)
            return render(request, 'task/taskAddSuccessful.html')
              
    # Fetch the requester's project
    # For example, if the user is logged in, you can retrieve their project from the logged-in user
    todouser = todoUser.objects.get(user = request.user)
    requester_projects = Project.objects.filter(TeamLeader=todouser)

    context = {
        'requester_project': requester_projects,  # Pass requester's project to the template
        'project_members': project_members  # Pass project members to the template
    }

    return render(request, 'task/taskProjectadd.html', context)

