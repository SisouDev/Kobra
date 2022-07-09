from collections import defaultdict

from django.core.exceptions import ValidationError


class AuthorPostValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_description()
        self.clean_intro()
        cd = self.data
        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self.errors['title'].append(
                'Title and description must be different'
            )
            self.errors['description'].append(
                'Title and description must be different'
            )

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')
        if len(title) < 5:
            self.errors['title'].append('Title is too short')
        return title

    def clean_description(self):
        description = self.data.get('description')
        try:
            if len(description) < 20:
                self.errors['description'].append('Description is too short')
        except (TypeError, ValueError):
            self.errors['description'].append('Description is not a string')
        return description

    def clean_intro(self):
        intro = self.data.get('intro')
        try:
            if len(intro) < 20:
                self.errors['intro'].append('Intro is too short')
        except (TypeError, ValueError):
            self.errors['intro'].append('Intro is not a string')
        return intro
