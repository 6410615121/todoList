from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import todoUser, Friend_request


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


'''
class FriendRequestViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass2'
        )
        self.todo_user1 = todoUser.objects.create(
            user=self.user1,
            Firstname='User1',
            Lastname='One',
        )
        self.todo_user2 = todoUser.objects.create(
            user=self.user2,
            Firstname='User2',
            Lastname='Two',
        )

    def test_send_friend_request_view(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('send_friend_request', args=[str(self.todo_user2.todoUser_ID)]))
        self.assertEqual(response.status_code, 200)
        

    def test_accept_friend_request_view(self):
        friend_request = Friend_request.objects.create(
            From_user=self.todo_user1,
            To_user=self.todo_user2,
        )

        self.client.force_login(self.user2)
        response = self.client.post(reverse('accept_friend_request', args=[str(self.todo_user1.todoUser_ID)]))
        self.assertEqual(response.status_code, 200)
'''       

