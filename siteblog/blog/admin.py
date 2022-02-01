from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # Auto create of Slug
    form = PostAdminForm  # For ckeditor
    save_on_top = True
    list_display = ('id', 'title', 'category', 'created_at', 'views', 'get_photo', 'author',)
    list_display_links = ('id', 'title',)
    list_filter = ('category', 'author', )
    search_fields = ('title',)
    fields = ('title', 'slug', 'author', 'category', 'tags', 'content', 'get_photo', 'views', 'created_at',)
    readonly_fields = ('created_at', 'views', 'get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<a href="{obj.photo.url}"><img src="{obj.photo.url}" width="80"></a>')
        return '-'

    get_photo.short_description = 'Фото'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
