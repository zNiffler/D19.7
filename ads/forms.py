from django import forms
from django.forms import ClearableFileInput

from ads.models import Ad, Response


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'author', 'title', 'text', 'content']
        widgets = {
            'content': ClearableFileInput(attrs={'multiple': True}),
        }


class ResForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
