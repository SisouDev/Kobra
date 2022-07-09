from collections import defaultdict
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from posts.models import Post
from utils.django_forms import add_placeholder, strong_password
from .validators import AuthorPostValidator


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['password'], 'Be strong!')

    password2 = forms.CharField(
        label='Repeat password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password.'
        }),
        error_messages={
            'required': 'This field cannot be empty.',
        },
        help_text=(
            'This field is required.'
        ),
    )

    username = forms.CharField(
        label='Username',
        help_text='Required. 150 characters or fewer\
            letters digits and @/./+/-/_ only.',
        error_messages={
            'required': 'This field cannot be empty.',
            'min_length': 'Username must be at least 4 characters.',
            'max_length': 'Username must be 150 characters or fewer.',
        },
        max_length=150, min_length=4,
    )

    first_name = forms.CharField(
        error_messages={
            'required': 'This field is required.'
        },
        required=True,
        label='First name',
        max_length=150,
        min_length=5,
    )

    email = forms.EmailField(
        error_messages={
            'required': 'This field is required.'
        },
        required=True,
        label='E-mail',
        help_text='Enter valid email address',
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'This field is required.'
        },
        required=True,
        label='Last name',
        max_length=150,
        min_length=5,
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        validators=[strong_password],
        help_text='This field is required.',
        label='Password',
        error_messages={
            'required': 'This field cannot be empty.'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'username': 'Required. 150 characters or fewer\
            letters digits and @/./+/-/_ only.',
            'email': 'Enter valid email address',
            'password': 'This field is required.',
        }

        error_messages = {
            'email': {
                'required': 'This field cannot be empty.',
                'invalid': 'Enter valid email address',
            },
            'username': {
                'required': 'This field cannot be empty.',
            },
            'first_name': {
                'required': 'This field cannot be empty.',
            },
        }

        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'This name %(value)s is invalid.',
                code='invalid',
                params={'value': 'John Doe'}
            )

        if 'Jane Doe' in data:
            raise ValidationError(
                'This name %(value)s is invalid.',
                code='invalid',
                params={'value': 'Jane Doe'}
            )
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password does not match.',
                'password2': 'Password does not match.',
            })


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class AuthorPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

    class Meta:
        model = Post
        fields = 'title', 'description', 'intro', \
            'content', 'cover', 'image_post'

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorPostValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
