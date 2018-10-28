from django import forms

from services import models


class VisaCreateForm(forms.ModelForm):
    class Meta:
        model = models.Visa
        exclude = ['client']
        widgets = {
            'passport_no': forms.TextInput(attrs={'class': 'form-control'}),
            'visa_no': forms.TextInput(attrs={'class': 'form-control'}),
            'extension_request_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'passport_expiration_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'passport_issuance_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'visa_expiration_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'visa_issuance_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'
        widgets = {
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'civil_status': forms.Select(attrs={'class': 'form-control'}),
            'naturalness': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'father': forms.TextInput(attrs={'class': 'form-control'}),
            'mother': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'md-textarea', 'rows': 2}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'data_attachment': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
            'born_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
