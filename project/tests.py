from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import todoUser
from project.models import Project
from task.models import Task
from .form import ProjectTaskEditForm
from django.utils import timezone

class ProjectViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.todo_user = todoUser.objects.create(user=self.user, Firstname='Test', Lastname='User')

        #create a friend
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        another_todo_user = todoUser.objects.create(user=another_user, Firstname='Another', Lastname='User')

        self.todo_user.friends.add(another_todo_user)


        # Login the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpass')




    def test_projectAdd_view(self):
        response = self.client.get(reverse('projectAdd'))
        self.assertEqual(response.status_code, 200)

        # Assuming friend_id exists
        friend_id = self.todo_user.friends.first()
        friend_id = friend_id.todoUser_ID

        # add friend
        response = self.client.post(reverse('projectAdd'), {
            'submit_add_member': 'true',
            'friend': friend_id
        })
        self.assertEqual(response.status_code, 200)

        # test remove added friend
        response = self.client.post(reverse('projectAdd'), {
            'remove_added_member': friend_id,
        })
        self.assertEqual(response.status_code, 200)

        # add friend again
        response = self.client.post(reverse('projectAdd'), {
            'submit_add_member': 'true',
            'friend': friend_id
        })
        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse('projectAdd'), {
            'submit_add_project': 'true',
            'project_name': 'Test Project'
        })
        
        self.assertRedirects(response, reverse('ProjectList')) 




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


class ProjectTaskViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test todoUser
        self.todouser = todoUser.objects.create(user=self.user, Firstname='Test', Lastname='User')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Create a test project
        project = Project.objects.create(Project_name='testproject', TeamLeader=self.todouser)
        project.TeamMember.add(self.todouser)

        # create a test task in project
        task = Task.objects.create(Project=project, TeamUser=self.todouser, task_title='test_task', Teamleader=self.todouser)


    def test_project_task_detail_view(self):

        # get project and task
        project = Project.objects.first()
        task = project.tasks_project.first()


        response = self.client.get(reverse('project_task_detail', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 200)


    def test_project_task_submit_view(self):
        # get project and task
        project = Project.objects.first()
        task = project.tasks_project.first()

        #submit
        response = self.client.post(reverse('project_task_submit', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 302)

        updated_task = Task.objects.get(Task_ID=task.Task_ID)
        self.assertTrue(updated_task.achieve)


        #unsubmit
        response = self.client.post(reverse('project_task_submit', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 302)

        updated_task = Task.objects.get(Task_ID=task.Task_ID)
        self.assertFalse(updated_task.achieve)
        
    def test_delete_project_task_view(self):
        # get project and task
        project = Project.objects.first()
        task = project.tasks_project.first()
        
        response = self.client.get(reverse('delete_project_task', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 302)


    def test_delete_project_task_view_noPermission(self):
        # get project and task
        project = Project.objects.first()
        task = project.tasks_project.first()
        
        another_user = User.objects.create_user(username='testuser2', password='testpassword')
        another_todoUser = todoUser.objects.create(user=another_user, Firstname='testuser2', Lastname='testpassword')
        
        self.client = Client()
        self.client.login(username='testuser2', password='testpassword')

        response = self.client.get(reverse('delete_project_task', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 403)




    def test_project_task_edit_view(self):
        # get project and task
        project = Project.objects.first()
        task = project.tasks_project.first()

        form_data = {
            'task_title': 'new_title',
            'description': 'new_description',
            'TeamUser': task.TeamUser.todoUser_ID,
            'Due_Date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        }

        form = ProjectTaskEditForm(data=form_data, instance=task, initial={'TeamUser': task.TeamUser}, project=task.Project)

        # getting
        response = self.client.get(reverse('project_task_edit', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 200)

        # editing
        response = self.client.post(reverse('project_task_edit', kwargs={'task_id': task.Task_ID}), data=form_data)

        # Check that the form is valid
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)

        # Reload the task from the database
        updated_task = Task.objects.get(Task_ID=task.Task_ID)

        # Check that task_title has changed
        self.assertEqual(updated_task.task_title, 'new_title')


    def test_project_task_edit_view_noPermission(self):
        # get project and task
        project = Project.objects.first()
        task = project.tasks_project.first()
        
        another_user = User.objects.create_user(username='testuser2', password='testpassword')
        another_todoUser = todoUser.objects.create(user=another_user, Firstname='testuser2', Lastname='testpassword')
        
        self.client = Client()
        self.client.login(username='testuser2', password='testpassword')

        response = self.client.get(reverse('project_task_edit', kwargs={'task_id': task.Task_ID}))
        self.assertEqual(response.status_code, 403)

    def test_delete_project_view(self):
        project = Project.objects.first()
        response = self.client.post(reverse('project_delete', kwargs={'project_id': project.Project_ID}))
        self.assertEqual(response.status_code, 302)

    def test_delete_project_view_noPermission(self):
        project = Project.objects.first()

        another_user = User.objects.create_user(username='testuser2', password='testpassword')
        another_todoUser = todoUser.objects.create(user=another_user, Firstname='testuser2', Lastname='testpassword')
        
        self.client = Client()
        self.client.login(username='testuser2', password='testpassword')

        response = self.client.post(reverse('project_delete', kwargs={'project_id': project.Project_ID}))
        self.assertEqual(response.status_code, 403)




class ProjectEditViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test todoUser
        self.todouser = todoUser.objects.create(user=self.user, Firstname='Test', Lastname='User')

    def test_project_edit_view(self):
        # Create a test project with the test user as the leader
        project = Project.objects.create(Project_name='testproject', TeamLeader=self.todouser)
        project.TeamMember.add(self.todouser)

        # Log in the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Get the project_edit URL for the test project
        url = reverse('project_edit', kwargs={'project_id': project.Project_ID})

        # Simulate a POST request to edit the project
        response = self.client.post(url, {
            'Project_name': 'new_testproject',
            'remove_member': '',  # Handle empty string for remove_member
            'friend': '',  # Handle empty string for friend
            'added_member': '',  # Handle empty string for added_member
        })

        # Check that the response status code is 200 (OK) or 302 (Redirect) if you have a redirect after successful edit
        self.assertIn(response.status_code, [200, 302])

        # Reload the project from the database
        updated_project = Project.objects.get(Project_ID=project.Project_ID)

        # Check that the project name has changed
        self.assertEqual(updated_project.Project_name, 'new_testproject')

        # You can add more assertions based on your specific logic in the view

    # Add more test cases as needed