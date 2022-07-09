from django.urls import resolve, reverse
from posts.views import site

from .test_post_base import PostTestBase


class PostsHomeViewTest(PostTestBase):
    def test_post_home_views_function_is_correct(self):
        view = resolve(reverse('posts:home'))
        self.assertIs(view.func, site.home)

    def test_post_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('posts:home'))
        self.assertEqual(response.status_code, 200)

    def test_post_home_view_loads_correct_template(self):
        response = self.client.get(reverse('posts:home'))
        self.assertTemplateUsed(response, 'posts/basis.html')

    def test_post_template_home_shows_nothing_here_if_no_posts(self):
        response = self.client.get(reverse('posts:home'))
        self.assertIn(
            'Nothing Here.',
            response.content.decode('utf-8')
        )

    def test_post_home_template_loads_posts(self):
        ...

    def test_post_home_template_dont_load_is_published(self):
        self.make_post(is_published=False)
        response = self.client.get(reverse('posts:home'))
        self.assertIn(
            'Nothing Here.',
            response.content.decode('utf-8')
        )
