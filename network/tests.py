from django.test import Client, TestCase

from .models import User, Post, Like

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

    # Setup database with data
    def setUp(self):
        user1 = User.objects.create(username="user1", password="user1", email="user1@gmail.com")

    # index View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that index page renders
    def test_index(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    # login View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that login page renders
    def test_login(self):
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)

    # Test that login fails when username is invalid
    def test_login_fail_username_invalid(self):
        response = self.client.post("/login", {
            "username": "user",
            "password": "user1"
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["message"], "Invalid username and/or password.")

    # Test that login fails when password is invalid
    def test_login_fail_password_invalid(self):
        response = self.client.post("/login", {
            "username": "user1",
            "password": "user"
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["message"], "Invalid username and/or password.")

    # Test that login fails when username and password are invalid
    def test_login_fail_both_invalid(self):
        response = self.client.post("/login", {
            "username": "user",
            "password": "user"
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["message"], "Invalid username and/or password.")

    # Test that login is successful
    def test_login_success(self):
        response = self.client.post("/login", {
            "username": "user1",
            "password": "user1"
        })

        self.assertEquals(response.status_code, 200)

    # logout View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that user is logged out
    def test_logout(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.get("/logout")

        self.assertEquals(response.status_code, 302)

    # register View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that register page renders
    def test_register(self):
        response = self.client.get("/register")

        self.assertEqual(response.status_code, 200)
    
    # Test that registration fails when passwords do not match
    def test_register_fail_password_mismatch(self):
        response = self.client.post("/register", {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "1234",
            "confirmation": "123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Passwords must match.")

    # Test that registration fails when username is already taken
    def test_register_fail_username_in_use(self):
        response = self.client.post("/register", {
            "username": "user1",
            "email": "user2@gmail.com",
            "password": "1234",
            "confirmation": "1234"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Username already taken.")

    # Test that registration is sucessful
    def test_register_sucess(self):
        response = self.client.post("/register", {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "1234",
            "confirmation": "1234"
        })

        self.assertEqual(response.status_code, 302)

    # posts View Tests
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Test that a new post is not created when the post is empty
    def test_posts_new_post_content_empty(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        
        response = self.client.post("/posts", {"content": ""}, "application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Post cannot be empty.")

    # Test that a new post is created successfully
    def test_posts_new_post_success(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        
        response = self.client.post("/posts", {"content": "content"}, "application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Post created successfully.")

    # Test that zero posts are retrieved when there are no posts
    def test_posts_get_nothing(self):
        response = self.client.get("/posts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    # Test that posts are retrieved when there are posts
    def test_posts_get_many(self):
        user = User.objects.get(username="user1")
        Post.objects.create(poster=user, content="This is my first post!")
        Post.objects.create(poster=user, content="This is my second post!")
        
        response = self.client.get("/posts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    # Test that nothing happens when the request method is PUT
    def test_posts_invalid_request_method(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        
        response = self.client.put("/posts")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "GET or POST request required.")

    # user_posts View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that nothing happens when request is POST
    def test_user_posts_request_method_is_post(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.post("/posts/user/user1")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "GET request required.")

    # Test that nothing happens when request is PUT
    def test_user_posts_request_method_is_put(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.put("/posts/user/user1")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "GET request required.")

    # Test that nothing happens when user does not exist
    def test_user_posts_user_does_not_exist(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.get("/posts/user/user2")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "User does not exist.")

    # Test that zero posts are retrieved when a user has no posts
    def test_user_posts_get_nothing(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.get("/posts/user/user1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    # Test that posts are retrieved when a user has posts
    def test_user_posts_get_many(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        Post.objects.create(poster=user, content="This is my first post!")
        Post.objects.create(poster=user, content="This is my second post!")

        response = self.client.get("/posts/user/user1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(data[0]["poster"], "user1")
        self.assertEqual(data[0]["content"], "This is my second post!")
        self.assertEqual(data[1]["poster"], "user1")
        self.assertEqual(data[1]["content"], "This is my first post!")
    
    # user View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that nothing happens when request is POST
    def test_user_request_method_is_post(self):
        response = self.client.post("/user1")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "GET request required.")

    # Test that nothing happens when user does not exist
    def test_user_user_does_not_exist(self):
        response = self.client.get("/user2")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "User does not exist.")

    # Test that info about a user is retrieved
    def test_user_get_info(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        user1.followers.add(user2)

        response = self.client.get("/user1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["username"], "user1")
        self.assertEqual(data["email"], "user1@gmail.com")
        self.assertEqual(len(data["followers"]), 1)
        self.assertEqual(len(data["following"]), 0)
    
    # Test that nothing happens when user trying to be followed/unfollowed does not exist
    def test_user_user_to_follow_or_unfollow_does_not_exist(self):
        response = self.client.put("/user1", {
            "follow": False,
            "user": "user2"
        }, "application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "User that is trying to be followed/unfollowed does not exist.")
    
    # Test that user is followed
    def test_user_user_is_followed(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        
        response = self.client.put("/user1", {
            "follow": True,
            "user": "user2"
        }, "application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "user1 is now following user2")
        self.assertEqual(user1.following.count(), 1)
        self.assertEqual(user2.followers.count(), 1)

    # Test that user is unfollowed
    def test_user_user_is_unfollowed(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        user1.followers.add(user2)
        
        response = self.client.put("/user1", {
            "follow": False,
            "user": "user2"
        }, "application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "user1 is no longer following user2")
        self.assertEqual(user1.following.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    # user_following_posts View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that nothing happens when request is POST
    def test_user_following_posts_request_method_is_post(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.post("/posts/user/user1/following")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "GET request required.")
    
    # Test that nothing happens when request is PUT
    def test_user_following_posts_request_method_is_put(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.put("/posts/user/user1/following")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "GET request required.")
    
    # Test that nothing happens when user does not exist
    def test_user_following_posts_user_does_not_exist(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.get("/posts/user/user2/following")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "User does not exist.")
    
    # Test that zero posts are retrieved when a user does not follow anyone
    def test_user_following_posts_follows_no_one(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)

        response = self.client.get("/posts/user/user1/following")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    # Test that zero posts are retrieved when people a user follows do not have any posts
    def test_user_following_posts_get_nothing(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        user3 = User.objects.create(username="user3", password="user3", email="user3@gmail.com")
        user2.followers.add(user1)
        user3.followers.add(user1)
        user2.save()
        user3.save()

        response = self.client.get("/posts/user/user1/following")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
  
    # Test that posts are retrieved when people a user follows have posts
    def test_user_following_posts_get_many(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        user3 = User.objects.create(username="user3", password="user3", email="user3@gmail.com")
        user2.followers.add(user1)
        user3.followers.add(user1)
        user2.save()
        user3.save()

        Post.objects.create(poster=user2, content="user2 post")
        Post.objects.create(poster=user3, content="user3 post")

        response = self.client.get("/posts/user/user1/following")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(data[0]["poster"], "user3")
        self.assertEqual(data[0]["content"], "user3 post")
        self.assertEqual(data[1]["poster"], "user2")
        self.assertEqual(data[1]["content"], "user2 post")

    # update_post View Tests
    # ---------------------------------------------------------------------------------------------
    # Test that nothing happens when request is GET
    def test_update_post_request_method_is_get(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        response = self.client.get("/posts/1/update")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "PUT request required.")


    # Test that nothing happens when request is POST
    def test_update_post_request_method_is_post(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        response = self.client.post("/posts/1/update")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "PUT request required.")

    # Test that nothing happens when post does not exist
    def test_update_post_post_does_not_exist(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        response = self.client.put("/posts/1/update", {"content": "updated content"}, "application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Post does not exist.")


    # Test that nothing happens when user that made the request is not the post's poster
    def test_update_post_request_user_is_not_the_poster(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        self.client.force_login(user1)

        Post.objects.create(poster=user2, content="original content")

        response = self.client.put("/posts/1/update", {"content": "updated content"}, "application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "You do not have access to edit this post.")
    
    # Test that post is not updated when the post is empty
    def test_update_post_post_content_empty(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        Post.objects.create(poster=user1, content="original content")

        response = self.client.put("/posts/1/update", {"content": ""}, "application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Post cannot be empty.")

    # Test that the content of the post is updated
    def test_update_post_post_content_updated(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        Post.objects.create(poster=user1, content="original content")

        response = self.client.put("/posts/1/update", {"content": "updated content"}, "application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Content of post successfully updated.")
        self.assertEqual(user1.posts.first().content, "updated content")
    
    # Test that a like is added to the post
    def test_update_post_like_post(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        post = Post.objects.create(poster=user1, content="original content")

        response = self.client.put("/posts/1/update", {"like": True}, "application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Added like to post 1.")
        self.assertEqual(user1.likes.first().post, post)
        self.assertEqual(post.likes.first().liker, user1)

    # Test that a like is removed from the post
    def test_update_post_unlike_post(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        post = Post.objects.create(poster=user1, content="original content")
        Like.objects.create(post=post, liker=user1)

        response = self.client.put("/posts/1/update", {"like": False}, "application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Removed like from post 1.")
        self.assertEqual(user1.likes.all().count(), 0)
        self.assertEqual(post.likes.all().count(), 0)
    