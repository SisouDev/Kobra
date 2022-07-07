from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def get_by_id(self, web_element, id_element):
        return web_element.find_element(
            By.XPATH,
            f'//*[@id="{id_element}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div/div/div/div/div/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)

        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_id(form, "id_first_name")
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_id(form, "id_last_name")
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field is required.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_id(form, "id_username")
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field cannot be empty.', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_id(form, "id_email")
            email_field.send_keys('email@email')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Enter valid email address', form.text)
        self.form_field_test_with_callback(callback)

    def test_password_match_error_message(self):
        def callback(form):
            password1_field = self.get_by_id(form, "id_password")
            password2_field = self.get_by_id(form, "id_password2")
            password1_field.send_keys('P@ssw0rd')
            password2_field.send_keys('P@ssw0rd_different')
            password2_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password does not match.', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_data_valid_register_sucess(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_id(form, "id_first_name").send_keys('First Name')
        self.get_by_id(form, "id_last_name").send_keys('Last Name')
        self.get_by_id(form, "id_username").send_keys('Myusername')
        self.get_by_id(form, "id_email").send_keys('email@valid.com')
        self.get_by_id(form, "id_password").send_keys('P@ssw0rd1')
        self.get_by_id(form, "id_password2").send_keys('P@ssw0rd1')
        self.get_by_id(form, "id_password2").send_keys(Keys.ENTER)

        self.assertIn(
            'Account registered successfully.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
