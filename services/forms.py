from django import forms

from services import models


class VisaCreateForm(forms.ModelForm):
    class Meta:
        model = models.Visa
        exclude = ['client', 'status']
        widgets = {
            'specification': forms.Select(attrs={'class': 'form-control custom-select'}),
            'request_type': forms.Select(attrs={'class': 'form-control custom-select'}),
            'passport_no': forms.TextInput(attrs={'class': 'form-control'}),
            'visa_no': forms.TextInput(attrs={'class': 'form-control'}),
            'extension_request_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'passport_expiration_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'passport_issuance_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'visa_expiration_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'visa_issuance_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }


class PassportCreateForm(forms.ModelForm):
    class Meta:
        model = models.Passport
        exclude = ['client', 'status']
        widgets = {
            'passport_issuance_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'passport_expiration_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'emission_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'remission_date': forms.TextInput(attrs={'class': 'datepicker'}),
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


class EntityForm(forms.ModelForm):
    class Meta:
        model = models.Entity
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'localization': forms.TextInput(attrs={'class': 'form-control'}),
            'identification_no': forms.TextInput(attrs={'class': 'form-control'}),
            'issuance_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
