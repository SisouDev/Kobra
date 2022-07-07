from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(
        default="PY",
        max_length=65,
        choices=(
            ('PY', 'Python'),
            ('JS', 'JavaScript'),
            ('FW', 'FrameWorks'),
            ('JV', 'Java'),
            ('OT', 'Others')
        )
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True, blank=True, null=True)
    intro = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField()
    content_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='posts/covers/%Y/%m/%d/', default='', blank=True, null=True,
    )
    image_post = models.ImageField(
        upload_to='posts/image_post/%Y/%m/%d/', null=True,
        blank=True, default='',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default='',
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)
