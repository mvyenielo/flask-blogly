import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()



class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        print('SELF.USER_ID =',self.user_id)
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_delete_user(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')


    # def test_delete_user_followed(self):
    #     with self.client as c:
    #         resp = c.get("/users", follow_redirects = True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("test1_first", html)
    #         self.assertNotIn("test1_last", html)

    def test_submit_user_edit(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/edit',
                          data={'first_name': 'edited_first_name',
                                'last_name': 'edited_last_name', 'image_url': ''})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')
            print(resp)
            print(resp.get_data)


    # def test_submit_user_edit_followed(self):
    #     with self.client as c:
    #         resp = c.get("/users", follow_redirects = True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("edited_first_name", html)
    #         self.assertNotIn("edited_last_name", html)

    def test_show_user_info(self):
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_user_edit(self):
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit a user</h1>", html)




class PostViewTestCase(TestCase):
    """Test views for post."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        test_post = Post(
            title="test_title",
            content="test_content",
            user_id=test_user.id,
        )

        db.session.add(test_user)
        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

        print('SELF.USER_ID =',self.user_id)
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_show_new_post_form(self):
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/posts/new')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h2> Add Post for test1_first test1_last </h2>", html)

    def test_submit_new_post(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/posts/new',
                          data={'title': 'new_title',
                                'content': 'new_content',
                                'user_id': f'{self.user_id}'})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'/users/{self.user_id}')

    def test_submit_edit_post(self):
        with self.client as c:
            resp = c.post(f'/posts/{self.post_id}/edit',
                          data={'title': 'edited_title',
                                'content': 'edited_contet',
                                'user_id': f'{self.user_id}'})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'/posts/{self.post_id}')
            # print("******Response from test_submit_edit_post: ", resp)
            # print("******Response .get_data from test_submit_edit_post: ",resp.get_data)






