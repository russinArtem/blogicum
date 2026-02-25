from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'short_title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'pub_date',
        'is_published',
        'location',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category', 'author')

    def short_title(self, object):
        return object.title[:30]
    short_title.short_description = 'Заголовок'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'short_title',
        'description',
        'is_published',
    )
    list_editable = (
        'description',
        'is_published',
    )

    def short_title(self, object):
        return object.title[:30]
    short_title.short_description = 'Заголовок'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'short_name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )

    def short_name(self, object):
        return object.name[:30]
    short_name.short_description = 'Название места'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'short_name',
        'post',
        'author',
        'created_at',
    )
    list_filter = ('post', 'author')

    def short_name(self, object):
        return object.name[:100]
    short_name.short_description = 'Текст комментария'
