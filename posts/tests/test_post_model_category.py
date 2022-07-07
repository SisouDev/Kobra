from .test_post_base import PostTestBase


class PostCategoryModelTest(PostTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_post_category_model_string_repr(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )
