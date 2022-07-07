from django.test import TestCase
from posts.models import Category, Post, User


class PostMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user123y',
        last_name='name234',
        username='usernamee',
        password='123456',
        email='username@emerail.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_post(
        self,
        category_data=None,
        author_data=None,
        title='Post Title',
        description='Post Description',
        slug='um-dois',
        intro='introducao',
        content='conteudo',
        content_is_html=False,
        is_published=True,
        cover='',
        image_post='',
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Post.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            intro=intro,
            content=content,
            content_is_html=content_is_html,
            is_published=is_published,
            cover=cover,
            image_post=image_post
        )

    def make_post_in_batch(self, qtd=10):
        posts = []
        for i in range(qtd):
            kwargs = {
                'title': f'Post Title {i}',
                'slug': f'r{i}*2',
                'author_data': {'username': f'u{i}'},
                'description': f'{i} aaaaaaa',
            }
            post = self.make_post(**kwargs)
            posts.append(post)
        return posts


class PostTestBase(TestCase, PostMixin):
    def setUp(self) -> None:
        return super().setUp()
