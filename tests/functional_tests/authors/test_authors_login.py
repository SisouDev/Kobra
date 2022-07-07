from .base import AuthorsBaseTest
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def get_by_id(self, web_element, id_element):
        return web_element.find_element(
            By.XPATH,
            f'//*[@id="{id_element}"]'
        )

    def test_user_valid_data_login_sucess(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user',
            password=string_password
        )
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(
            By.ID, 'main-form'
        )

        username_field = self.get_by_id(form, 'id_username')
        password_field = self.get_by_id(form, 'id_password')
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)
        password_field.send_keys(Keys.ENTER)

        self.assertIn(
            'Your are logged in as:\n>> " My_user " <<',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )
        self.assertIn(
            'Not Found',
            self.browser.find_element(
                By.TAG_NAME, 'body'
            ).text
        )

    def test_login_form_is_invalid(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        form = self.browser.find_element(
            By.ID, 'main-form'
        )
        username_field = self.get_by_id(form, 'id_username')
        password_field = self.get_by_id(form, 'id_password')

        username_field.send_keys(' ')
        password_field.send_keys(' ')
        password_field.send_keys(Keys.ENTER)

        self.assertIn(
            'Error to validate form data.',
            self.browser.find_element(
                By.TAG_NAME, 'body'
            ).text
        )

    def test_login_invalid_crendentials(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )
        form = self.browser.find_element(
            By.ID, 'main-form'
        )
        username_field = self.get_by_id(form, 'id_username')
        password_field = self.get_by_id(form, 'id_password')

        username_field.send_keys('invalid_user')
        password_field.send_keys('invalid_password')
        password_field.send_keys(Keys.ENTER)

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(
                By.TAG_NAME, 'body'
            ).text
        )
