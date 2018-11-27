from django import forms

from services import models
from . import widgets


class VisaCreateForm(forms.ModelForm):
    class Meta:
        model = models.Visa
        exclude = ['client', 'status']
        widgets = {
            'specification': widgets.Select(),
            'request_type': widgets.Select(),
            'passport_no': widgets.TextInput(),
            'visa_no': widgets.TextInput(),
            'extension_request_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),
            'passport_issuance_date': widgets.DateInput(),
            'visa_expiration_date': widgets.DateInput(),
            'visa_issuance_date': widgets.DateInput(),
        }


class PassportCreateForm(forms.ModelForm):
    class Meta:
        model = models.Passport
        exclude = ['client', 'status']
        widgets = {
            'passport_type': widgets.Select(),
            'emission_date': widgets.DateInput(),
            'remission_type': widgets.Select(),
            'remission_date': widgets.DateInput(),
            'personal_no': widgets.TextInput(),
            'passport_no': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),
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
            'name': widgets.TextInput(),
            'localization': widgets.TextInput(),
            'identification_no': widgets.TextInput(),
            'issuance_date': widgets.DateInput(),
            'expiration_date': widgets.DateInput(),
            'telephone': widgets.TextInput(),
            'email': widgets.EmailInput(),
        }


class ResidenceAuthorizationForm(forms.ModelForm):
    class Meta:
        model = models.ResidenceAuthorization
        exclude = ['client', 'status']
        widgets = {
            'authorization_no': widgets.NumberInput(),
            'issued_place': widgets.TextInput(),
            'issuance_date': widgets.DateInput(),
            'valid_date': widgets.DateInput(),
            'passport_no': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),
        }


class ResidenceMarriageForm(forms.ModelForm):
    class Meta:
        model = models.ResidenceMarriage
        exclude = ['client', 'status']
        widgets = {
            'married_to': widgets.TextInput(),
            'ci': widgets.TextInput(),
            'issuance_date': widgets.DateInput(),
            'valid_date': widgets.DateInput(),
        }


class ResidenceRenovationForm(forms.ModelForm):
    class Meta:
        model = models.ResidenceRenovation
        exclude = ['client', 'status']
        widgets = {
            'residence_authorization_no': widgets.TextInput(),
            'issuance_date': widgets.DateInput(),
            'expiration_date': widgets.DateInput(),
            'reason': widgets.Select(),
            'passport_no': widgets.TextInput(),
            'issuance_passport_date': widgets.DateInput(),
            'valid_passport_date': widgets.DateInput(),
        }
