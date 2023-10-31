from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class PostAdminForm(forms.ModelForm):
    """Form for the PostAdmin to use CKEditor for the content field."""

    content = forms.CharField(label='Вміст', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""

    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    """Admin configuration for the Tag model."""

    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model."""

    prepopulated_fields = {"slug": ("title",)}  # Auto create of Slug
    form = PostAdminForm  # For ckeditor
    save_on_top = True
    list_display = ('id', 'title', 'category', 'created_at', 'views', 'get_photo', 'author',)
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'author',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'author', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at',
              'notify_subscribers',)
    readonly_fields = ('created_at', 'views', 'get_photo',)

    def get_photo(self, obj):
        """Custom method to display the photo as a thumbnail in the admin list view."""
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width="80"></a>')
        return '-'

    get_photo.short_description = 'Мініатюра'


class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model."""

    pass


class SubscriberAdmin(admin.ModelAdmin):
    """Admin configuration for the Subscriber model."""

    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
