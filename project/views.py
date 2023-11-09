from django.shortcuts import render
from django.contrib.sessions.models import Session
from .models import todoUser, Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
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
                    print(project_name)
                else:
                    return render(request, 'project/projectAdd.html', context)
                
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