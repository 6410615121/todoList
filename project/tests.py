from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import todoUser
from project.models import Project
from task.models import Task

class ProjectViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.todo_user = todoUser.objects.create(user=self.user, Firstname='Test', Lastname='User')

        # Login the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpass')




    def test_projectAdd_view(self):
        response = self.client.get(reverse('projectAdd'))
        self.assertEqual(response.status_code, 200)

        # Assuming friend_id exists
        friend_id = str(self.todo_user.friends.first().todoUser_ID)
        response = self.client.post(reverse('projectAdd'), {
            'submit_add_member': 'true',
            'friend': friend_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')  # Adjust based on your actual template

        response = self.client.post(reverse('projectAdd'), {
            'submit_add_project': 'true',
            'project_name': 'Test Project'
        })
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after submission




    def test_ProjectList_view(self):
        response = self.client.get(reverse('ProjectList'))
        self.assertEqual(response.status_code, 200)



    def test_project_detail_view(self):
        # Create a test project
        test_project = Project.objects.create(Project_name='Test Project', TeamLeader=self.todo_user)

        # Create a test task associated with the project
        test_task = Task.objects.create(Project=test_project, Teamleader=self.todo_user, TeamUser=self.todo_user,
                                        task_title='Test Task')

        response = self.client.get(reverse('project_detail', kwargs={'project_id': test_project.Project_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Test Task')

