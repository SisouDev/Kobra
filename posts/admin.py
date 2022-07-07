from django.contrib import admin

from .models import Category, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published']
    list_display_links = ['title', 'created_at']
    search_fields = 'id', 'title', 'description', 'content'
    list_filter = 'category', 'author', 'is_published', 'content_is_html'
    list_per_page = 10
    list_editable = 'is_published',
    prepopulated_fields = {
        'slug': ('title',)
    }
    autocomplete_fields = 'tags',


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
