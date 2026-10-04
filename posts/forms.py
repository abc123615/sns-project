from django import forms
from .models import Post, Profile, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']