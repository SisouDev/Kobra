from django.urls import resolve, reverse
from posts import views

from .test_post_base import PostTestBase


class PostDetailViewTest(PostTestBase):
    def test_post_post_views_function_is_correct(self):
        view = resolve(reverse('posts:post', kwargs={
            'id': 1,
        }))
        self.assertIs(view.func, views.post)

    def test_post_post_returns_404_if_dont_have(self):
        response = self.client.get(
            reverse('posts:post', kwargs={
                'id': 100
            })
        )
        self.assertEqual(response.status_code, 404)

    def test_post_detail_template_dont_load_post_dont_published(self):
        post = self.make_post(is_published=False)
        response = self.client.get(
            reverse(
                'posts:post',
                kwargs={
                    'id': post.id
                }
            )
        )
        self.assertEqual(response.status_code, 404)
