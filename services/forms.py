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
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'born_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'civil_status': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.ImageField(),
            'father': forms.TextInput(attrs={'class': 'form-control'}),
            'mother': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_attachment': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
            # work data
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'funcion': forms.TextInput(attrs={'class': 'form-control'}),
            'work_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Current address
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'commune': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'home_no': forms.TextInput(attrs={'class': 'form-control'}),
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


class ServiceStatusFrom(forms.Form):
    REQUEST_TYPE_CHOICES = (
        ('passport', _('Passport')),
        ('visa', _('Visa')),
        ('residence', _('Residence')),
    )
    request_type = forms.ChoiceField(choices=REQUEST_TYPE_CHOICES)
    search = forms.CharField()

    def search_status(self):
        request_type = self.cleaned_data['request_type']
        search = self.cleaned_data['search']
        if request_type == 'passport':  # passport, search by ci
            results = models.Passport.objects.filter(
                Q(ci__exact=search)
            )
            if results:
                results_done = results.filter(Q(status=models.Service.SERVICE_STATUS[4][0]))
                if results_done:
                    data = []
                    for i in results_done:
                        data.append({'client_name': i.client.get_full_name(), 'passport_no': i.passport_no})
                    results = data
                else:
                    return {'message': _('It is in process')}
            else:
                results = {}
        elif request_type == 'visa':  # visa, search by passport no
            results = models.Visa.objects.filter(Q(passport_no__exact=search))
            if results:
                results_done = results.filter(Q(status=models.Service.SERVICE_STATUS[4][0]))
                if results_done:
                    data = []
                    for i in results_done:
                        data.append({'client_name': i.client.get_full_name(), 'passport_no': i.passport_no})
                    results = data
                else:
                    return {'message': _('It is in process')}
            else:
                results = {}
        elif request_type == 'residence':  # all residence, search by passport no
            authorization = models.ResidenceAuthorization.objects.filter(Q(passport_no__exact=search))

            if authorization:
                authorization_done = authorization.filter(Q(status=models.Service.SERVICE_STATUS[4][0]))
                if authorization_done:
                    results = []
                    for i in authorization_done:
                        results.append({'client_name': i.client.get_full_name(), 'passport_no': i.passport_no})
                else:
                    return {'message': _('It is in process')}
            else:
                results = {}
        else:
            results = {}  # raise error
        return {} if results == [] else {'data': results}
