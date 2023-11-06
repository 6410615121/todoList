from django.test import TestCase
from .models import todoUser
from django.contrib.auth.models import User

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
