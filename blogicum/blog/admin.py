from django.contrib import admin

from .models import Post, Category, Location

admin.site.empty_value_display = 'Не задано'


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

    def short_title(self, obj):
        return obj.title[:30]
    short_title.short_description = 'Заголовок'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


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

    def short_title(self, obj):
        return obj.title[:30]
    short_title.short_description = 'Заголовок'


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

    def short_name(self, obj):
        return obj.name[:30]
    short_name.short_description = 'Название места'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
