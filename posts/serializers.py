from rest_framework import serializers
from .models import Category
from tag.models import Tag
from .models import Post
from authors.validators import AuthorPostValidator


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title',
            'description',
            'intro', 'category',
            'author', 'tags',
        ]
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
    )
    author = serializers.StringRelatedField(
        read_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
    )

    def validate(self, attrs):
        if self.instance is not None and attrs.get('intro') is None:
            attrs['intro'] = self.instance.intro
        if self.instance is not None and attrs.get('description') is None:
            attrs['description'] = self.instance.description

        super_validate = super().validate(attrs)
        AuthorPostValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError
        )
        return super_validate
