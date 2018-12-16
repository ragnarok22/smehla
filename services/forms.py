from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

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


class ServiceStatusFrom(forms.Form):
    REQUEST_TYPE_CHOICES = (
        ('national', _('National')),
        ('foreigner', _('Foreigner')),
    )
    SEARCH_TYPE_CHOICES = (
        ('ci', _('Identity Card')),
        ('passport', _('Passport')),
        ('residence', _('Number of Residence')),
    )
    request_type = forms.ChoiceField(choices=REQUEST_TYPE_CHOICES)
    search_type = forms.ChoiceField(choices=SEARCH_TYPE_CHOICES)
    search = forms.CharField()

    def search_status(self):
        search_type = self.cleaned_data['search_type']
        search = self.cleaned_data['search']
        if self.cleaned_data['request_type'] == 'national':  # visa passport
            if search_type == 'ci':
                visa_result = models.Visa.objects.filter(
                    Q(client__ci__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
                passport_result = models.Passport.objects.filter(
                    Q(client__ci__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
            elif search_type == 'passport':
                visa_result = models.Visa.objects.filter(
                    Q(passport_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
                passport_result = models.Passport.objects.filter(
                    Q(passport_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
            else:
                visa_result = []
                passport_result = []
            results = []
            for v in visa_result:
                results.append({
                    'client_name': v.client.get_full_name(),
                    'passport_no': v.passport_no
                })
            for p in passport_result:
                results.append({
                    'client_name': p.client.get_full_name(),
                    'passport_no': p.passport_no
                })
        elif self.cleaned_data['request_type'] == 'foreigner':  # renovation marriage authorization
            if search_type == 'passport':
                renovation_result = models.ResidenceRenovation.objects.filter(
                    Q(passport_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
                marriage_result = models.ResidenceMarriage.objects.filter(
                    Q(passport_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
                authorization_result = models.ResidenceAuthorization.objects.filter(
                    Q(passport_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
            elif search_type == 'residence':
                renovation_result = models.ResidenceRenovation.objects.filter(
                    Q(residence_authorization_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
                marriage_result = models.ResidenceMarriage.objects.filter(
                    Q(passport_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
                authorization_result = models.ResidenceAuthorization.objects.filter(
                    Q(authorization_no__exact=search) & Q(status=models.Service.SERVICE_STATUS[4][0])
                )
            else:
                renovation_result = []
                marriage_result = []
                authorization_result = []
            results = []
            for r in renovation_result:
                results.append({
                    'client_name': r.client.get_full_name(),
                    'passport_no': r.passport_no
                })
            for m in marriage_result:
                results.append({
                    'client_name': m.client.get_full_name(),
                    'passport_no': m.passport_no
                })
            for a in authorization_result:
                results.append({
                    'client_name': a.client.get_full_name(),
                    'passport_no': a.passport_no
                })
        else:
            results = []  # raise error
        return {} if results == [] else {'data': results}
