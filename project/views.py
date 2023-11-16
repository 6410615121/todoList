from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.sessions.models import Session
from .models import todoUser, Project
from task.models import Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction


@login_required
def projectAdd(request):
    memberAdded_ids = request.session.get('memberAdded', [])
    todouser = todoUser.objects.get(user=request.user)
    friendList = todouser.friends.all()

    memberAdded_names = []  # Store added members' names

    if request.method == 'POST':
        if 'submit_add_member' in request.POST:
            friend_ID = request.POST.get('friend')
            if not friend_ID in memberAdded_ids:
                memberAdded_ids.append(friend_ID)
                request.session['memberAdded'] = memberAdded_ids

        if 'submit_add_project' in request.POST:
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
                    return render(request, 'project/projectAdd.html', context)
                
            if memberAdded_ids:
                request.session.pop('memberAdded')
            return redirect('ProjectList')

    for member_id in memberAdded_ids:
        # Retrieve the todoUser object for each ID and extract the name
        member = get_object_or_404(todoUser, todoUser_ID=member_id)
        memberAdded_names.append(member.Firstname +' '+ member.Lastname) 

    context = {
        'memberAdded': memberAdded_names,
        'friendList': friendList,
    }
    
    return render(request, 'project/createproject.html', context)


@login_required
def ProjectList(request):
    todouser = todoUser.objects.get(user=request.user)
    projects_with_user = Project.objects.filter(TeamMember=todouser)


    context = {
        'projects_with_user': projects_with_user,
        
    }
    
    return render(request, 'project/projectlist.html', context)

@login_required
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
    }
    return render(request,'project/project_detail.html', context)


@login_required
def project_task_detail(request, task_id):
    
    mytasks = Task.objects.get(Task_ID=task_id)

    context = {
        'taskdetail': mytasks,
    }
    return render(request,'project/project_task_detail.html', context)


@login_required
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
    
    context = {
        'taskdetail': mytask,
        
    }
    return render(request,'task/task_detail.html', context)