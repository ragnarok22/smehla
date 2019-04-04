from django import forms

from news import models


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control md-textarea'}),
        }


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Service
        exclude = ['service']
        widgets = {
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
