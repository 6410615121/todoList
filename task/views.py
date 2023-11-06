from django.shortcuts import render ,redirect
from .form import TaskForm
from .models import Project,Task, Individual_Task
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import todoUser
# Create your views here.

def taskIndex(request):
    return render(request, 'task/taskIndex.html')

def taskList(request):
    todouser = todoUser.objects.get(user=request.user)
    projects_with_user = Project.objects.filter(TeamMember=todouser)

    tasks_by_project = {}
    for project in projects_with_user:
        tasks = Task.objects.filter(Project=project)
        tasks_by_project[project.Project_ID] = tasks  # Use project ID as the key

    context = {
        'projects_with_user': projects_with_user,
        'tasks_by_project': tasks_by_project,
    }

    return render(request, 'task/taskList.html', context)



def task_add(request):
    project_members = None
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        selected_project = request.POST.get('project')
        if selected_project is not None:
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

    return render(request, 'task/taskAdd.html', context)

def individual_taskAdd(request):
    if request.method == 'POST':
        todouser = todoUser.objects.get(user = request.user)

        task_title = request.POST.get('task_title')
        Due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        Individual_Task.objects.create(User = todouser, task_title = task_title, Due_Date = Due_date, description = description)
        
        return render(request, 'task/taskAddSuccessful.html')

    return render(request, 'task/individual_taskAdd.html')