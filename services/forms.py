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
            'passport_no': widgets.TextInput(),
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
                Q(client__ci__exact=search)
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
            marriage = models.ResidenceMarriage.objects.filter(Q(passport_no__exact=search))
            authorization = models.ResidenceAuthorization.objects.filter(Q(passport_no__exact=search))
            renovation = models.ResidenceRenovation.objects.filter(Q(passport_no__exact=search))

            if marriage or authorization or renovation:
                marriage_done = marriage.filter(Q(status=models.Service.SERVICE_STATUS[4][0]))
                authorization_done = authorization.filter(Q(status=models.Service.SERVICE_STATUS[4][0]))
                renovation_done = renovation.filter(Q(status=models.Service.SERVICE_STATUS[4][0]))

                if marriage_done or authorization_done or renovation_done:
                    data = []
                    if marriage_done:
                        for i in marriage_done:
                            data.append({'client_name': i.client.get_full_name(), 'passport_no': i.passport_no})
                    if authorization_done:
                        for i in authorization_done:
                            data.append({'client_name': i.client.get_full_name(), 'passport_no': i.passport_no})
                    if renovation_done:
                        for i in renovation_done:
                            data.append({'client_name': i.client.get_full_name(), 'passport_no': i.passport_no})
                    results = data
                else:
                    return {'message': _('It is in process')}
            else:
                results = {}
        else:
            results = {}  # raise error
        return {} if results == [] else {'data': results}
