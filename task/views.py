from django.shortcuts import render ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse ,Http404 ,HttpResponseRedirect, HttpResponseForbidden
from user.models import todoUser
from project.models import Project
from .models import Individual_Task ,Task
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from task.form import IndividualTaskEditForm
from project.views import project_task_detail
#from django.utils.http import quote

import os
# Create your views here.
@login_required(login_url='login')
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
        mytask = sorted(
            Individual_Task.objects.filter(User=mytodouser, category='due'),
            key=lambda x: x.time_difference
        )
    elif cat == "past":
        mytask = sorted(
            Individual_Task.objects.filter(User=mytodouser, category='pastdue'),
            key=lambda x: x.time_difference
        )
    elif cat == "com":
        mytask = sorted(
            Individual_Task.objects.filter(User=mytodouser, category='complete'),
            key=lambda x: x.time_difference
        )
    
    return   mytask

@login_required(login_url='login')
def delete_individual_task(request, task_id):
    task = Individual_Task.objects.get(Task_ID = task_id)
    task_owner = task.User
    todouser_request = todoUser.objects.get(user = request.user)

    if task_owner != todouser_request:
        return HttpResponseForbidden("You don't have permission to delete this task.")
    
    task.delete()
    return redirect('individual_tasklist')



@login_required(login_url='login')
def individual_tasklist(request):
    mytask = updatetask(request,"due")      

        
    context = {'tasklist': mytask}
    
    return render(request, 'task/task.html',context)

@login_required(login_url='login')
def individual_past_tasklist(request):
    mytask = updatetask(request,"past")      

        
    context = {'tasklist': mytask}
    
    return render(request, 'task/pastduetask.html',context)

@login_required(login_url='login')
def individual_com_tasklist(request):
    mytask = updatetask(request,"com")      

        
    context = {'tasklist': mytask}
    
    return render(request, 'task/completetask.html',context)

@login_required(login_url='login')
def individual_taskAdd(request):
    if request.method == 'POST':
        todouser = todoUser.objects.get(user = request.user)

        task_title = request.POST.get('task_title')
        Due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        Individual_Task.objects.create(User = todouser, task_title = task_title, Due_Date = Due_date, description = description)
        
        return individual_tasklist(request)

    return render(request, 'task/individual_taskAdd.html')



@login_required(login_url='login')
def task_add(request,project_ID):
    selected_project = Project.objects.get(Project_ID = project_ID)
    project_members = selected_project.TeamMember.all() 
    todouser = todoUser.objects.get(user = request.user)
    if request.method == 'POST':
      
        selected_Owner = request.POST.get('task_owner')
        selected_Owner = todoUser.objects.get(todoUser_ID = selected_Owner)
        task_title = request.POST.get('task_title')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        Task.objects.create(Project = selected_project, Teamleader=todouser ,TeamUser = selected_Owner, task_title = task_title, Due_Date = due_date, description = description)
            
    todouser = todoUser.objects.get(user = request.user)
    requester_projects = Project.objects.filter(TeamLeader=todouser)

    context = {
        'requester_project': requester_projects,  # Pass requester's project to the template
        'project_members': project_members  # Pass project members to the template
    }

    return render(request, 'task/taskProjectadd.html',context)

@login_required(login_url='login')
def task_detail(request, task_id):
    
    mytask = Individual_Task.objects.get(Task_ID=task_id)
   
    context = {
        'taskdetail': mytask,
        
    }
    return render(request,'task/task_detail.html', context)

# for using in pythonanywhere
'''
@login_required(login_url='login')
def download_file(request, task_id):
    instance = get_object_or_404(Individual_Task, Task_ID=task_id)

    try:
        # PythonAnywhere-specific modification
        filename = quote(instance.file.name)  # Update the function name
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        instance.file.open(mode='rb')
        response.write(instance.file.read())
        instance.file.close()

        return response
    except FileNotFoundError:
        raise Http404("File not found")
'''
@login_required(login_url='login')
def download_file(request, task_id):
    instance = get_object_or_404(Individual_Task, Task_ID=task_id)

    response = HttpResponse(instance.file.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{instance.file.name}"'
    return response

@login_required(login_url='login')
def upload_file(request ,task_id):
    if request.method == 'POST':
        project = False
        mytask = Individual_Task.objects.filter(Task_ID=task_id).first()
        
        if mytask is None:
            mytask = Task.objects.filter(Task_ID=task_id).first()
            project = True
        
        uploaded_file = request.FILES.get('file_task')
        filename = uploaded_file.name
        
        mytask.file.save(filename, uploaded_file)


        return project_task_detail(request, task_id) if project else task_detail(request, task_id)
    

@login_required(login_url='login')
def submit(request, task_id):
    mytask = Individual_Task.objects.get(Task_ID=task_id)
    if request.method == 'POST':
        if mytask.achieve == True:
            mytask.achieve = False  # undo submit 
            mytask.category = 'due'
        else:
            mytask.achieve = True   # submit
            mytask.category = 'complete'

        mytask.save()
    return HttpResponseRedirect(reverse('task_detail', kwargs={'task_id': task_id}))
    
    # context = {
    #     'taskdetail': mytask,
        
    # }
    # return render(request,'task/task_detail.html', context)


@login_required(login_url='login')
def individual_task_edit(request, task_id):
    task = get_object_or_404(Individual_Task, Task_ID=task_id)

    if request.method == 'POST':
        form = IndividualTaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            
    form = IndividualTaskEditForm(instance=task)
    context = {'form': form, 'task_id': task_id}
    return render(request, 'task/individual_task_edit.html', context)
