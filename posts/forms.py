from django import forms
from .models import Post, Profile, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(
        max_length=500,
        required=True,
        strip=True,
        widget=forms.Textarea
    )

    class Meta:
        model = Post
        fields = ['content']


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        max_length=300,
        required=False,
        strip=True,
        widget=forms.Textarea
    )

    class Meta:
        model = Profile
        fields = ['bio']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=350,
        required=True,
        strip=True,
        widget=forms.Textarea
    )

    class Meta:
        model = Comment
        fields = ['content']