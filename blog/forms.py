from django import forms

from .models import Post
from . import models
from django.forms import ModelForm, TextInput, Textarea


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")
