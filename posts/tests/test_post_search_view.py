from django.urls import reverse
from .test_post_base import PostTestBase


class PostSearchViewsTest(PostTestBase):
    def test_post_search_loads_correct_template(self):
        response = self.client.get(reverse('posts:search') + '?q=teste')
        self.assertTemplateUsed(
            response, 'posts/search.html'
        )

    def test_post_search_raises_404_if_dont_have_term(self):
        response = self.client.get(reverse('posts:search'))
        self.assertEqual(response.status_code, 404)

    def test_post_search_term_is_on_page_title_and_escaped(self):
        url = reverse('posts:search') + '?q=teste'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;teste&quot;',
            response.content.decode('utf-8')
        )

    def test_post_search_can_find_post_by_title(self):
        ...
