from django.test import TestCase
from django.urls import reverse, resolve
from posts import views


class PostURLsTest(TestCase):
    def test_post_home_url_is_correct(self):
        home_url = reverse('posts:home')
        self.assertEqual(home_url, '/')

    def test_post_category_url_is_correct(self):
        category_url = reverse('posts:category', kwargs={
            'category_id': 1,
        })
        self.assertEqual(category_url, '/posts/category/1/')

    def test_post_post_url_is_correct(self):
        post_url = reverse('posts:post', kwargs={
            'id': 1,
        })
        self.assertEqual(post_url, '/posts/1/')

    def test_post_search_url_is_correct(self):
        search_url = reverse('posts:search')
        self.assertEqual(search_url, '/posts/search/')

    def test_post_search_loads_correct_view_function(self):
        resolved = resolve(reverse('posts:search'))
        self.assertIs(resolved.func, views.search)
