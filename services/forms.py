from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from services import models
from . import widgets


class VisaCreateForm(forms.ModelForm):
    class Meta:
        model = models.Visa
        exclude = ['client', 'status', 'official', 'request_type']
        widgets = {
            'process_no': widgets.NumberInput(),
            # client data
            'place_of_birth': widgets.TextInput(),
            'birth_country': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'current_nationality': widgets.TextInput(),
            # passport data
            'passport_no': widgets.TextInput(),
            'passport_issuance_place': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),

            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            'lodging': widgets.TextInput(),
            'city_lodging': widgets.TextInput(),
            'street_lodging': widgets.TextInput(),
            'no_lodging_house': widgets.TextInput(),
            'last_entry_angola_date': widgets.DateInput(),
            'frontier': widgets.TextInput(),
            'visa_expiration_date': widgets.DateInput(),
        }


class MedicalTreatmentVisaForm(forms.ModelForm):
    class Meta:
        model = models.MedicalTreatmentVisa
        exclude = ['client', 'status', 'official', 'request_type']
        widgets = {
            'process_no': widgets.NumberInput(),
            # client data
            'place_of_birth': widgets.TextInput(),
            'birth_country': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'current_nationality': widgets.TextInput(),
            # passport data
            'passport_no': widgets.TextInput(),
            'passport_issuance_place': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),

            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            'lodging': widgets.TextInput(),
            'city_lodging': widgets.TextInput(),
            'street_lodging': widgets.TextInput(),
            'no_lodging_house': widgets.TextInput(),
            'last_entry_angola_date': widgets.DateInput(),
            'frontier': widgets.TextInput(),
            'visa_expiration_date': widgets.DateInput(),

            'unity_medical_name': widgets.TextInput(),
            'unity_type': widgets.Select(),
            'date_init_treatment': widgets.DateInput(),
            'data_end_treatment': widgets.DateInput(),
        }


class TemporaryVisaForm(forms.ModelForm):
    class Meta:
        model = models.TemporaryVisa
        exclude = ['client', 'status', 'official', 'request_type']
        widgets = {
            'process_no': widgets.NumberInput(),
            # client data
            'place_of_birth': widgets.TextInput(),
            'birth_country': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'current_nationality': widgets.TextInput(),
            # passport data
            'passport_no': widgets.TextInput(),
            'passport_issuance_place': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),

            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            'lodging': widgets.TextInput(),
            'city_lodging': widgets.TextInput(),
            'street_lodging': widgets.TextInput(),
            'no_lodging_house': widgets.TextInput(),
            'last_entry_angola_date': widgets.DateInput(),
            'frontier': widgets.TextInput(),
            'visa_expiration_date': widgets.DateInput(),

            'reason': widgets.Select(),
            'subsistence': widgets.TextInput(),
            'address_angola': widgets.TextInput(),
        }


class StudyVisaForm(forms.ModelForm):
    class Meta:
        model = models.StudyVisa
        exclude = ['client', 'status', 'official', 'request_type']
        widgets = {
            'process_no': widgets.NumberInput(),
            # client data
            'place_of_birth': widgets.TextInput(),
            'birth_country': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'current_nationality': widgets.TextInput(),
            # passport data
            'passport_no': widgets.TextInput(),
            'passport_issuance_place': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),

            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            'lodging': widgets.TextInput(),
            'city_lodging': widgets.TextInput(),
            'street_lodging': widgets.TextInput(),
            'no_lodging_house': widgets.TextInput(),
            'last_entry_angola_date': widgets.DateInput(),
            'frontier': widgets.TextInput(),
            'visa_expiration_date': widgets.DateInput(),

            'study_program': widgets.Select(),
            'init_date': widgets.DateInput(),
            'end_date': widgets.DateInput(),
            'stages_in': widgets.Select(),
        }


class ExtensionVisaForm(forms.ModelForm):
    class Meta:
        model = models.ExtensionVisa
        exclude = ['client', 'status', 'official']
        widgets = {
            'process_no': widgets.NumberInput(),
            'request_type': widgets.Select(),
            # client data
            'place_of_birth': widgets.TextInput(),
            'birth_country': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'current_nationality': widgets.TextInput(),
            # passport data
            'passport_no': widgets.TextInput(),
            'passport_issuance_place': widgets.TextInput(),
            'passport_issuance_date': widgets.DateInput(),
            'passport_expiration_date': widgets.DateInput(),

            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            'lodging': widgets.TextInput(),
            'city_lodging': widgets.TextInput(),
            'street_lodging': widgets.TextInput(),
            'no_lodging_house': widgets.TextInput(),
            'last_entry_angola_date': widgets.DateInput(),
            'frontier': widgets.TextInput(),
            'visa_expiration_date': widgets.DateInput(),

            'visa_no': widgets.TextInput(),
            'valid_date': widgets.DateInput(),
            'reason_extension': widgets.TextInput(),
            # responsible
            'name': widgets.TextInput(),
            'province': widgets.TextInput(),
            'city': widgets.TextInput(),
            'neighborhood': widgets.TextInput(),
            'street_no': widgets.TextInput(),
            'home_no': widgets.TextInput(),
            'phone': widgets.TextInput(),
            'email': widgets.EmailInput(),
        }


class PassportCreateForm(forms.ModelForm):
    class Meta:
        model = models.Passport
        exclude = ['client', 'status', 'official']
        widgets = {
            'process_no': widgets.NumberInput(),
            'passport_type': widgets.Select(),
            'act_type': widgets.Select(),
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
            'first_name': widgets.TextInput(),
            'last_name': widgets.TextInput(),
            'born_date': widgets.DateInput(),
            'civil_status': widgets.Select(),
            'sex': widgets.Select(),
            'picture': forms.FileInput(),
            'father': widgets.TextInput(),
            'mother': widgets.TextInput(),
            'email': widgets.EmailInput(),
            'phone': widgets.NumberInput(),
            'data_attachment': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
            # work data
            'profession': widgets.TextInput(),
            'funcion': widgets.TextInput(),
            'work_name': widgets.TextInput(),
            'province_work': widgets.TextInput(),
            'neighborhood_work': widgets.TextInput(),
            'email_work': widgets.EmailInput(),
            'phone_work': widgets.NumberInput(),
            # Current address
            'province': widgets.TextInput(),
            'municipality': widgets.TextInput(),
            'commune': widgets.TextInput(),
            'street': widgets.TextInput(),
            'home_no': widgets.TextInput(),
            # birth address
            'province_birth': widgets.TextInput(),
            'municipality_birth': widgets.TextInput(),
            'commune_birth': widgets.TextInput(),
            'neighborhood_birth': widgets.TextInput(),
            'street_birth': widgets.TextInput(),
            'home_no_birth': widgets.TextInput(),
            # Filiation
            'father_nationality': widgets.TextInput(),
            'mother_nationality': widgets.TextInput(),
            'nationality': widgets.TextInput(),
            'current_nationality': widgets.TextInput(),
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
        if request_type == 'passport':  # passport, search by ci or cedula pesoal
            results = models.Passport.objects.filter(
                Q(ci__exact=search) | Q(cp__exact=search)
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
