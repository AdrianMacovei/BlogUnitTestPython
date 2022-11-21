from unittest import TestCase
from unittest.mock import patch
import app
from blog import Blog
from post import Post


class AppTest(TestCase):
    def setUp(self):
        blog = Blog('Test', 'Test Author')
        app.blogs = {'Test': blog}

    def test_menu_calls_create_blog(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('c', 'Test Create Blog', 'Test Author', 'q')

            app.menu()

            self.assertIsNotNone(app.blogs['Test Create Blog'])

    def test_menu_calls_ask_create_post(self):
        blog = app.blogs['Test']
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('r', 'Test', 'Post title', 'Post content', 'q')

            app.menu()
            self.assertIsNotNone(blog.posts)

    def test_menu_calls_read_blog(self):
        blog = app.blogs['Test']
        blog.create_post('Post Title', 'Post content')
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('r', 'Test', 'q')
            with patch('builtins.print') as mocked_print:

                app.menu()
                mocked_print.assert_called_with('\n    ---Post Title---\n    \n    Post content\n    \n')

    def test_menu_calls_print_blogs(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('l', 'Test', 'q')
            with patch('builtins.print') as mocked_print:

                app.menu()
                mocked_print.assert_called_with('-Test by Test Author (0 posts)')

    def test_menu_print_prompt(self):
        with patch('builtins.input', return_value='q') as mocked_input:
            app.menu()
            mocked_input.assert_called_with(app.MENU_PROMPT)

    def test_menu_print_blogs(self):
        with patch('app.print_blogs') as mocked_print_blogs:
            with patch('builtins.input', return_value='q'):
                app.menu()
                mocked_print_blogs.assert_called_with()

    def test_print_blogs(self):
        with patch('builtins.print') as mocked_print:
            app.print_blogs()
            mocked_print.assert_called_with('-Test by Test Author (0 posts)')

    def test_ask_create_blog(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Author')
            app.ask_create_blogs()

            self.assertIsNotNone(app.blogs.get('Test'))

    def test_ask_read_blog(self):
        blog = app.blogs['Test']
        with patch('builtins.input', return_value='Test'):
            with patch('app.print_posts') as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_with(blog)

    def test_print_posts(self):
        blog = app.blogs['Test']
        blog.create_post('Post Title', 'Post Content')

        with patch('app.print_post') as mocked_print_post:
            app.print_posts(blog)
            mocked_print_post.assert_called_with(blog.posts[0])

    def test_print_post(self):
        post = Post('Post title', 'Post content')
        expected_print = '''
    ---Post title---
    
    Post content
    
'''
        with patch('builtins.print') as mocked_print:
            app.print_post(post)

            mocked_print.assert_called_with(expected_print)

    def test_ask_create_post(self):

        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            app.ask_create_post()

            self.assertEqual(app.blogs['Test'].posts[0].title, 'Test Title')
            self.assertEqual(app.blogs['Test'].posts[0].content, 'Test Content')
