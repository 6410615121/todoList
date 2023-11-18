from django.utils import timezone
from .models import Task,Individual_Task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings




def check_and_update_tasks():
   
    Tasks_to_update = Task.objects.filter(category='due')
    Individual_Task_to_update = Individual_Task.objects.filter(category='due')
    
    
    for task in Tasks_to_update:
        print("check_and_update_tasks function is running")
        email = str(task.TeamUser.user.email)

        def createemaiform(task,days):
            content=f"""
            Dear {task.TeamUser.Firstname} {task.TeamUser.Lastname},

            I hope this message finds you well. This is a friendly reminder that you have a task scheduled for completion {days}. Time is of the essence, and we wanted to ensure you have ample notice to complete the task successfully.

            Task Details:

            Project Name: {task.Project.Project_name}
            Task Name: {task.task_title}
            Due Date: {task.Due_Date}

            Thank you for your attention to this matter. We appreciate your commitment to completing tasks promptly.

            """
            return content
        

        time_diff = max(task.Due_Date - timezone.now(), timedelta())  # Use max to ensure non-negative timedelta
        total_seconds = time_diff.total_seconds()
        days = int(total_seconds // 86400)  # 86400 seconds in a day
        if days == 1:
            send_mail('Complete Your Task Tomorrow!!!', createemaiform(task,"tommorow"), settings.EMAIL_HOST_USER,[email])
        elif days == 3:
            send_mail('Complete Your Task in 3 Days', createemaiform(task,"in the next 3 days"), settings.EMAIL_HOST_USER, [email])
        elif days == 7:
            send_mail('Complete Your Task in 7 Days', createemaiform(task,"in the next 7 days"), settings.EMAIL_HOST_USER, [email])
    
    for Intask in Individual_Task_to_update:
        email = str(Intask.User.user.email)

        def createemaiform(task,days):
            content=f"""
            Dear {task.TeamUser.Firstname} {task.TeamUser.Lastname},

            I hope this message finds you well. This is a friendly reminder that you have a task scheduled for completion {days}. Time is of the essence, and we wanted to ensure you have ample notice to complete the task successfully.

            Task Details:

            Task Name: {task.task_title}
            Due Date: {task.Due_Date}

            Thank you for your attention to this matter. We appreciate your commitment to completing tasks promptly.

            """
            return content
        
        time_diff = max(Intask.Due_Date - timezone.now(), timedelta())  # Use max to ensure non-negative timedelta
        total_seconds = time_diff.total_seconds()
        days = int(total_seconds // 86400)  # 86400 seconds in a day
        if days == 1:
            send_mail('Complete Your Task Tomorrow!!!', createemaiform(task,"tommorow"), settings.EMAIL_HOST_USER, [email])
        elif days == 3:
            send_mail('Complete Your Task in 3 Days', createemaiform(task,"in the next 3 days"), settings.EMAIL_HOST_USER, [email])
        elif days == 7:
            send_mail('Complete Your Task in 7 Days', createemaiform(task,"in the next 7 days"), settings.EMAIL_HOST_USER, [email])
    

