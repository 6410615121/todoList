from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import todoUser
from project.models import Project
from .models import Individual_Task

class TaskViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.todo_user = todoUser.objects.create(user=self.user, Firstname='Test', Lastname='User')

        # Create a test project
        self.project = Project.objects.create(Project_name='Test Project', TeamLeader=self.todo_user)

        # Create a test task
        due_date = timezone.make_aware(timezone.datetime(2023, 12, 31, 14, 30)) 
        self.task = Individual_Task.objects.create(User=self.todo_user, task_title='Test Task', Due_Date= due_date, description='Test Description')

        # Login the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_individual_tasklist_view(self):
        response = self.client.get(reverse('individual_tasklist'))
        self.assertEqual(response.status_code, 200)
        

    def test_individual_past_tasklist_view(self):
        # Assuming the Due_Date of the task is in the past
        due_date = timezone.make_aware(timezone.datetime(2022, 1, 1, 14, 30)) 
        self.task.Due_Date = due_date 
        self.task.save()

        response = self.client.get(reverse('individual_past_tasklist'))
        self.assertEqual(response.status_code, 200)
        

    def test_individual_com_tasklist_view(self):
        # Assuming the task is marked as 'complete'
        self.task.achieve = True
        self.task.save()

        response = self.client.get(reverse('individual_com_tasklist'))
        self.assertEqual(response.status_code, 200)
        

    def test_individual_taskAdd_view(self):
        due_date = timezone.make_aware(timezone.datetime(2023, 12, 31, 14, 30)) 
        response = self.client.post(reverse('individual_taskadd'), {
            'task_title': 'New Task',
            'due_date': due_date,
            'description': 'New Task Description'
        })
        self.assertEqual(response.status_code, 200)
        

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', kwargs={'task_id': self.task.Task_ID}))
        self.assertEqual(response.status_code, 200)
        

    def test_submit_view(self):
        response = self.client.post(reverse('submit', kwargs={'task_id': self.task.Task_ID}))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after submission
