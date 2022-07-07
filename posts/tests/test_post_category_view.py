from django.urls import resolve, reverse
from posts import views

from .test_post_base import PostTestBase


class PostCategoryViewTest(PostTestBase):
    def test_post_category_views_function_is_correct(self):
        view = resolve(reverse('posts:category', kwargs={
            'category_id': 1
        }))
        self.assertIs(view.func, views.category)

    def test_post_category_returns_404_not_found(self):
        response = self.client.get(
            reverse('posts:category', kwargs={
                'category_id': 100
            })
        )
        self.assertEqual(response.status_code, 404)

    def test_post_category_404_dont_published(self):
        post = self.make_post(is_published=False)
        response = self.client.get(
            reverse('posts:post', kwargs={
                'id': post.category.id
            })
        )
        self.assertEqual(response.status_code, 404)
