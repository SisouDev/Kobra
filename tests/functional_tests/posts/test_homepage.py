import pytest
from selenium.webdriver.common.by import By

from .base import PostBaseFunctionalTest


@pytest.mark.functional_test
class TestHomePageFunctional(PostBaseFunctionalTest):
    def test_home_page_without_posts_error_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nothing Here.', body.text)

    def test_home_page_pagination(self):
        self.browser.get(self.live_server_url)
