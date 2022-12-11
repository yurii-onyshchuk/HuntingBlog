from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'id': 'contactcomment', 'class': 'form-control', 'rows': '4', 'placeholder': 'Коментар'}), label='',
        min_length=5, max_length=500)

    class Meta:
        model = Comment
        fields = ('body',)
