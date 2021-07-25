from django.test import Client, TestCase

from .models import User, Post, Like

# Create your tests here.

# Test class for models
class ModelTest(TestCase):
    # Setup test database with data
    def setUp(self):
        user1 = User.objects.create(username="user1", password="user1", email="user1@gmail.com")
        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        user1.followers.add(user2)
        user2.followers.add(user1)

        post = Post.objects.create(poster=user1, content="This is my first post!")

        like = Like.objects.create(liker=user1, post=post)
    
    # Test that a User is initialized properly
    def test_user(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")

        self.assertEqual(user1.username, "user1")
        self.assertEqual(user1.password, "user1")
        self.assertEqual(user1.email, "user1@gmail.com")
        self.assertEqual(user1.followers.first(), user2)
        self.assertEqual(user2.followers.first(), user1)

    # Test that a Post is initialized properly
    def test_post(self):
        user = User.objects.get(username="user1")
        post = Post.objects.get(poster=user)

        self.assertEqual(post.poster, user)
        self.assertEqual(post.content, "This is my first post!")

    # Test that a Like is initialized properly
    def test_like(self):
        user = User.objects.get(username="user1")
        post = Post.objects.get(poster=user)
        like = Like.objects.get(liker=user)

        self.assertEquals(like.liker, user)
        self.assertEquals(like.post, post)

# Test class for client
class ClientTest(TestCase):

    client = Client()

    # Test that index view works
    def test_index(self):
        pass

    # Test that logout view works
    def test_logout_view(self):
        pass

    # Test that login view works
    def test_login_view(self):
        pass

    # Test that register view works
    def test_register(self):
        pass

    # Test that a new post is created successfully
    def test_new_post_success(self):
        pass

    # Test that a new post is not created (no content)
    def test_new_post_fail_empty(self):
        pass

    # Test that a new post is not created (not a POST request)
    def test_new_post_fail_bad_request(self):
        pass