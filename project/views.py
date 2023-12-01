from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.sessions.models import Session
from .models import todoUser, Project
from task.models import Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.db import transaction
from .form import ProjectTaskEditForm, ProjectEditForm
from django.core.exceptions import ValidationError


@login_required(login_url='login')
def projectAdd(request):
    memberAdded_ids = request.session.get('memberAdded', [])
    project_name_session = request.session.get('project_name', '')

    todouser = todoUser.objects.get(user=request.user)
    friendList = todouser.friends.all()

    memberAdded = []

    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        if project_name:
            project_name_session = project_name

        if 'submit_add_member' in request.POST:
            friend_ID = request.POST.get('friend')
            if not friend_ID in memberAdded_ids:
                memberAdded_ids.append(friend_ID)
                request.session['memberAdded'] = memberAdded_ids
        
        elif 'remove_added_member' in request.POST:
            friend_ID_to_remove = request.POST.get('remove_added_member')
            if friend_ID_to_remove in memberAdded_ids:
                memberAdded_ids.remove(friend_ID_to_remove)
                request.session['memberAdded'] = memberAdded_ids
                
                
        elif 'submit_add_project' in request.POST:
            project_name = request.POST.get('project_name')
            project_leader = todoUser.objects.get(user = request.user)
            finalmembers = [project_leader]
            for member_id in memberAdded_ids:
                # Retrieve the todoUser object for each ID and extract the name
                member = get_object_or_404(todoUser, todoUser_ID=member_id)
                finalmembers.append(member)

            with transaction.atomic():
                if project_name != '':
                    new_project = Project.objects.create(Project_name=project_name, TeamLeader= project_leader)
                    new_project.TeamMember.set(finalmembers)
                    
                    
                else:
                    return render(request, 'project/createproject.html', {
                        'memberAdded': memberAdded,
                        'friendList': friendList,
                        'project_name_session':project_name_session,
                    })
                
            if memberAdded_ids:
                request.session.pop('memberAdded')
                
            return redirect('ProjectList')                  


    for member_id in memberAdded_ids:
        # Retrieve the todoUser object for each ID and extract the name
        member = get_object_or_404(todoUser, todoUser_ID=member_id)
        memberAdded.append(member) 

    context = {
        'memberAdded': memberAdded,
        'friendList': friendList,
        'project_name_session':project_name_session,
    }
    
    return render(request, 'project/createproject.html', context)


@login_required(login_url='login')
def ProjectList(request):
    todouser = todoUser.objects.get(user=request.user)
    projects_with_user = Project.objects.filter(TeamMember=todouser)


    context = {
        'projects_with_user': projects_with_user,
        
    }
    
    return render(request, 'project/projectlist.html', context)

@login_required(login_url='login')
def project_detail(request, project_id):
    todouser = todoUser.objects.get(user = request.user)
    
    
    project_obj = Project.objects.get(Project_ID = project_id)
    tasks = project_obj.tasks_project.all()

    assignedtask = tasks.filter(TeamUser = todouser)
    other_tasks = tasks.exclude(TeamUser=todouser)
    context = {
        'project_obj': project_obj,
        'project_name': project_obj.Project_name,
        'assignedtask': assignedtask,
        'other_tasks': other_tasks,
        'authorization':todouser,
    }
    return render(request,'project/project_detail.html', context)


@login_required(login_url='login')
def project_task_detail(request, task_id):
    
    mytasks = Task.objects.get(Task_ID=task_id)
    todouser_request = todoUser.objects.get(user = request.user)

    context = {
        'taskdetail': mytasks,
        'authorization':todouser_request,
    }
    return render(request,'project/project_task_detail.html', context)


@login_required(login_url='login')
def submit(request, task_id):
    mytask = Task.objects.get(Task_ID=task_id)
    if request.method == 'POST':
        if mytask.achieve == True:
            mytask.achieve = False  # undo submit 
            mytask.category = 'due'
        else:
            mytask.achieve = True   # submit
            mytask.category = 'complete'

        mytask.save()
        return HttpResponseRedirect(reverse('project_task_detail', kwargs={'task_id': task_id}))
    
@login_required(login_url='login')
def mask_submit(request, task_id):
    mytask = Task.objects.get(Task_ID=task_id)
    if request.method == 'POST':
        if mytask.achieve == True:
            mytask.achieve = False  # undo submit 
            mytask.category = 'due'
        else:
            mytask.achieve = True   # submit
            mytask.category = 'complete'

        mytask.save()
        return project_detail(request,  mytask.Project.Project_ID)
    
    
@login_required(login_url='login')
def delete_project_task(request, task_id):
    task = Task.objects.get(Task_ID = task_id)
    task_owner = task.TeamUser
    todouser_request = todoUser.objects.get(user = request.user)

    if task_owner != todouser_request:
        return HttpResponseForbidden("You don't have permission to delete this task.")
    
    task.delete()
    return redirect('ProjectList')


@login_required(login_url='login')
def project_task_edit(request,task_id):
    task = get_object_or_404(Task, Task_ID=task_id)
    task_owner = task.TeamUser
    project_leader = task.Teamleader

    todouser_request = todoUser.objects.get(user = request.user)

    if task_owner != todouser_request and project_leader != todouser_request:
        return HttpResponseForbidden("You don't have permission to delete this task.")

    if request.method == 'POST':
        form = ProjectTaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

            
    form = ProjectTaskEditForm(instance=task, initial={'TeamUser': task.TeamUser}, project=task.Project)

    context = {'form': form,
               'task_id':task_id,
               }
               
    return render(request, 'project/project_task_edit.html',context)

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, Project_ID=project_id)
    
    todouser = todoUser.objects.get(user=request.user)
    friendList = todouser.friends.all()

    todouser_request = todoUser.objects.get(user=request.user)
    if project.TeamLeader != todouser_request:
        return HttpResponseForbidden("You don't have permission to edit this project.")
    
    if request.method == 'POST':
        form = ProjectEditForm(request.POST, instance=project, project=project)
        if form.is_valid():
            form.save()

        project_name = request.POST.get('Project_name')
        if project_name:
            project.Project_name = project_name
            project.save()

        team_member_remove_id = request.POST.get('remove_member')
        if team_member_remove_id:
            team_member_remove = get_object_or_404(todoUser, todoUser_ID=team_member_remove_id)

            if team_member_remove != project.TeamLeader:
                project.TeamMember.remove(team_member_remove)
                project.save()

        added_member = request.POST.get('friend')
        if added_member != 'None' and added_member != '':
            added_member = get_object_or_404(todoUser, todoUser_ID=added_member)
            project.TeamMember.add(added_member)
            project.save()
    
    form = ProjectEditForm(instance=project, project=project)


    context = {'form': form, 'project_id': project_id, 'friendList': friendList}
    
    return render(request, 'project/project_edit.html', context)


@login_required(login_url='login')
def delete_project(request, project_id):
    project = Project.objects.get( Project_ID = project_id)

    todouser_request = todoUser.objects.get(user=request.user)
    if project.TeamLeader != todouser_request:
        return HttpResponseForbidden("You don't have permission to delete this project.")
   
    project .delete()
    return redirect('ProjectList')