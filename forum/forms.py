from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']  # Champs pour le texte et l'image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  