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
