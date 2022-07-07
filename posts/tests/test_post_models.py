from .test_post_base import PostTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class PostModelTest(PostTestBase):
    def setUp(self) -> None:
        self.post = self.make_post()
        return super().setUp()

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('intro', 150),
    ])
    def test_post_fields_max_lenght(self, field, max_length):
        setattr(self.post, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.post.full_clean()