from unittest import TestCase
from post import Post


class PostTest(TestCase):

    p = Post('Test', 'Test Content')

    def test_create_post(self):

        self.assertEqual('Test', PostTest.p.title)
        self.assertEqual('Test Content', PostTest.p.content)

    def test_json(self):
        expected = {'title': 'Test', 'content': 'Test Content'}

        self.assertDictEqual(expected, PostTest.p.json())
