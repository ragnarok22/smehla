from django import forms

from news import models


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control textarea-md'}),
        }
