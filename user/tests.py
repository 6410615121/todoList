from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import todoUser, Friend_request, Forget_pass
from task.models import Task, Individual_Task
from project.models import Project

from .form import RegistrationForm

class UserViewsTest(TestCase):

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/about.html')

    def test_homepage_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        todo_user = todoUser.objects.create(user=user, Firstname='Test', Lastname='User')

        self.client.force_login(user)

        new_project = Project(
            Project_name="Your Project",
            TeamLeader=todo_user,
        )
        new_project.TeamMember.add(todo_user)
        new_project.save()

        Task.objects.create(
            Project=new_project,
            Teamleader=todo_user,
            TeamUser=todo_user,
            task_title="Your Task",
        )

        Individual_Task.objects.create(
            User = todo_user,
            task_title = 'mytask',
        )

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)



            
    def test_login_view_invalid(self):
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Test login with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


    def test_successful_login(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')
        todo_user = todoUser.objects.create(user=user, Firstname='Test', Lastname='User')

        response = self.client.get(reverse('login'))

        # Submit a POST request to the login view with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        # Check that the user is redirected to the homepage
        self.assertRedirects(response, reverse('homepage'))

        # Optionally, you can also check that the user is now logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)






class TodoUserTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test todoUser
        self.test_todo_user = todoUser.objects.create(user=self.test_user, Firstname='Test', Lastname='User')

    def test_user_has_todo_user(self):
        # Test if the user has a todoUser profile
        user_todo_user = todoUser.objects.get(user=self.test_user)
        self.assertEqual(user_todo_user, self.test_todo_user)

    def test_add_friend(self):
        # Create another user for testing
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')

        # Create a todoUser for another user
        another_todo_user = todoUser.objects.create(user=another_user, Firstname='Another', Lastname='User')

        # Add the second user as a friend to the first user
        self.test_todo_user.friends.add(another_todo_user)

        # Check if the second user is in the first user's friends list
        self.assertIn(another_todo_user, self.test_todo_user.friends.all())



class FriendRequestTest(TestCase):
    def setUp(self):
        # Create a test user to send or receive friend requests.
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.profile1 = todoUser.objects.create(user=self.user1, Firstname='John', Lastname='Doe')
        self.profile2 = todoUser.objects.create(user=self.user2, Firstname='Jane', Lastname='Smith')


    def test_send_friend_request(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('send_friend_request', kwargs={'userID': self.profile2.todoUser_ID}))
        self.assertEqual(response.status_code, 200)

        # Ensure a friend request is created
        friend_request = Friend_request.objects.filter(From_user=self.profile1, To_user=self.profile2).first()
        self.assertIsNotNone(friend_request)


    def test_accept_friend_request(self):
        # Create a friend request
        friend_request = Friend_request.objects.create(From_user=self.profile1, To_user=self.profile2)

        self.client.force_login(self.user2)
        self.client.get(reverse('accept_friend_request', kwargs={'userID': self.profile1.todoUser_ID}))
        

        # Ensure the friend request is accepted
        self.profile1.refresh_from_db()
        self.profile2.refresh_from_db()
        self.assertIn(self.profile1, self.profile2.friends.all())
        self.assertIn(self.profile2, self.profile1.friends.all())
        self.assertFalse(Friend_request.objects.filter(pk=friend_request.pk).exists())  # Friend request should be deleted because it was accepted

    def test_friend_request_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('friend request'))
        self.assertEqual(response.status_code,200)

        response = self.client.get(reverse('show_send_request'))
        self.assertEqual(response.status_code,200)

    def test_delete_friend(self):
        self.client.force_login(self.user1)
        self.profile1.friends.add(self.profile2)
        # self.profile2.friends.add(self.profile1)

        response = self.client.get(reverse('delete_friend', kwargs={'userID': self.profile2.todoUser_ID}))
        self.assertEqual(response.status_code,200)

    def test_unsend_friend_request(self):
        self.client.force_login(self.user1)
        self.client.get(reverse('send_friend_request', kwargs={'userID': self.profile2.todoUser_ID}))
       

        friend_request = Friend_request.objects.filter(From_user=self.profile1, To_user=self.profile2).first()
        response = self.client.get(reverse('unsend', kwargs={'userID': self.profile2.todoUser_ID}))
        






class RegistrationTest(TestCase):
    def test_registration_view(self):
        # Define test data
        registration_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.get(reverse('register'), registration_data)

        # Simulate a POST request to the registration view
        response = self.client.post(reverse('register'), registration_data)

        # Check if the registration was successful
        self.assertEqual(response.status_code, 302)  # Redirects after successful registration

        # Check if the user and todoUser are created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(todoUser.objects.filter(user=user).exists())
        todo_user = todoUser.objects.get(user=user)
        
        # Check additional details
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(todo_user.Firstname, 'John')
        self.assertEqual(todo_user.Lastname, 'Doe')



class profileTest(TestCase):
    def setUp(self):
        # Define test data
        registration_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }



        # Simulate a POST request to the registration view
        self.client.post(reverse('register'), registration_data)
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword123'})

    def test_editprofile_view(self):
        edit_data = {
            'Firstname': 'John1',
            'Lastname': 'Doe1',
            'Email': 'testuser1@example.com',
        }
        response = self.client.get(reverse('editprofile'))
        response = self.client.post(reverse('editprofile'), edit_data)

        self.assertRedirects(response, '/user/myaccount/')

    def test_find_user_view(self):
        # Create another user for testing
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')

        # Create a todoUser for another user
        another_todo_user = todoUser.objects.create(user=another_user, Firstname='Another', Lastname='User')

        #check that we can find exist user
        response = self.client.post(reverse('find_user'), {'user': 'anotheruser'})
        self.assertContains(response, "anotheruser")
        self.assertEqual(response.status_code, 200)

        #check that we can't find non-exist user
        response = self.client.post(reverse('find_user'), {'user': 'anotheruser123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no user")

    def test_resetpass_view(self):
        user = User.objects.get(username='testuser')
        request_new_pass = Forget_pass.objects.create(user = user)
        #password mismatch
        content ={
            'pass1': '1234',
            'pass2': '12345',
        }
        response = self.client.post(reverse('resetpass', kwargs={'requestID': request_new_pass.forget_ID}), content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'password mismatch')

        #password correct 
        content ={
            'pass1': '1234',
            'pass2': '1234',
        }

        response = self.client.get(reverse('resetpass', kwargs={'requestID': request_new_pass.forget_ID}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('resetpass', kwargs={'requestID': request_new_pass.forget_ID}), content)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '1234'})
        self.assertEqual(response.status_code, 302)
        
    def test_logout_view(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_forgetpass_view(self):
        response = self.client.get(reverse('forgetpass'))
        self.assertEqual(response.status_code, 200)

        content = {
            'email': User.objects.get(username='testuser').email
        }

        response = self.client.post(reverse('forgetpass'), content)
        self.assertEqual(response.status_code, 200)

    





        
        



