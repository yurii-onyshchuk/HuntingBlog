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
    list_display = ('id', 'title', 'category', 'created_at', 'views', 'photo',)
    list_display_links = ('id', 'title',)
    list_filter = ('category',)
    search_fields = ('title',)
    fields = ('title', 'slug', 'category', 'tags', 'content', 'photo', 'views', 'created_at',)
    readonly_fields = ('created_at', 'views', 'photo',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
