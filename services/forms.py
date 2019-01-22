from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from services import models
from . import widgets


class VisaCreateForm(forms.ModelForm):
    class Meta:
        model = models.Visa
        exclude = ['client', 'status', 'official']
        widgets = {
            'process_no': widgets.NumberInput(),
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


class WorkVisaForm(forms.ModelForm):
    class Meta:
        model = models.WorkVisa
        exclude = ['client', 'status', 'official']


class MedicalTreatmentVisaForm(forms.ModelForm):
    class Meta:
        model = models.MedicalTreatmentVisa
        exclude = ['client', 'status', 'official']


class ResidentVisaForm(forms.ModelForm):
    class Meta:
        model = models.ResidentVisa
        exclude = ['client', 'status', 'official']


class TemporaryVisaForm(forms.ModelForm):
    class Meta:
        model = models.TemporaryVisa
        exclude = ['client', 'status', 'official']


class PrivilegedVisaForm(forms.ModelForm):
    class Meta:
        model = models.PrivilegedVisa
        exclude = ['client', 'status', 'official']


class StudyVisaForm(forms.ModelForm):
    class Meta:
        model = models.StudyVisa
        exclude = ['client', 'status', 'official']


class ExtensionVisaForm(forms.ModelForm):
    class Meta:
        model = models.ExtensionVisa
        exclude = ['client', 'status', 'official']


class VisaRenovationForm(forms.ModelForm):
    class Meta:
        model = models.ExtensionVisa
        exclude = ['client', 'status', 'official']


class PassportCreateForm(forms.ModelForm):
    class Meta:
        model = models.Passport
        exclude = ['client', 'status', 'official']
        widgets = {
            'process_no': widgets.NumberInput(),
            'passport_type': widgets.Select(),
            'remission_type': widgets.Select(),
            # birth certificate
            'issued_in': widgets.TextInput(),
            # identity card
            'date': widgets.DateInput(),
            'cp': widgets.TextInput(),
            'cp_issued_in': widgets.TextInput(),
            'date_cp_issue': widgets.DateInput(),
            'ci': widgets.TextInput(),
            'ci_issued_in': widgets.TextInput(),
            'spouse': widgets.TextInput(),
            'observations': widgets.TextInput(),
            # client data, birth address
            'province_birth': widgets.TextInput(),
            'municipality_birth': widgets.TextInput(),
            'commune_birth': widgets.TextInput(),
            'neighborhood_birth': widgets.TextInput(),
            'street_birth': widgets.TextInput(),
            'home_no_birth': widgets.TextInput(),
            # for use of the reception
            'date_reception': widgets.DateInput(),
            # for official use
            'passport_no': widgets.TextInput(),
            'passport_issued_in': widgets.TextInput(),
            'date_issue_passport': widgets.DateInput(),
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
            # 'picture': forms.ImageField(),
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
        exclude = ['client', 'status', 'official']
        widgets = {
            'process_no': widgets.NumberInput(),
            'type_request': widgets.Select(),
            'extension_type': widgets.Select(),
            'observations': widgets.TextInput(),
            # Client data
            'naturalness': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'passport_no': widgets.TextInput(),
            'passport_issued_in': widgets.TextInput(),
            'date_issuance_passport': widgets.DateInput(),
            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            # for non-local use of reception
            'location': widgets.TextInput(),
            'date': widgets.DateInput(),
            # for official use
            'date_official_use': widgets.DateInput(),
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
