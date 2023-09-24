from django import forms
from apps.blog.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content', 'blog']