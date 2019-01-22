from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin

from accounts import mixins
from services import models, forms


class ServiceMixin(mixins.LoginRequiredMixin, SingleObjectMixin):
    service_type = None

    def dispatch(self, request, *args, **kwargs):
        self._set_attr_model(kwargs)
        return super(ServiceMixin, self).dispatch(request, *args, **kwargs)

    def _set_attr_model(self, kwargs):
        _type = kwargs.get('type')
        self.service_type = _type
        if _type == 'workvisa':
            self.model = models.WorkVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.WorkVisaForm
        elif _type == 'medicalvisa':
            self.model = models.MedicalTreatmentVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.MedicalTreatmentVisaForm
        elif _type == 'residentvisa':
            self.model = models.ResidentVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.ResidentVisaForm
        elif _type == 'temporaryvisa':
            self.model = models.TemporaryVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.TemporaryVisaForm
        elif _type == 'privilegedvisa':
            self.model = models.PrivilegedVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.PrivilegedVisaForm
        elif _type == 'studyvisa':
            self.model = models.StudyVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.StudyVisaForm
        elif _type == 'extensionvisa':
            self.model = models.ExtensionVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.ExtensionVisaForm
        elif _type == 'passport':
            self.model = models.Passport
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.PassportCreateForm
        elif _type == 'residence':
            self.model = models.ResidenceAuthorization
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.ResidenceAuthorizationForm
                self.template_name = 'services/residence_form.html'
        elif _type == 'extension':
            self.model = models.ExtensionVisa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.VisaRenovationForm
        else:
            raise Http404(_('Service type not found'))
        self.extra_context = {'type': _type}


class ServiceFormMixin(ServiceMixin, ModelFormMixin):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_type = self.service_type
        self.object.official = self.request.user
        self.object.client = models.Client.objects.get(pk=self.kwargs.get('pk'))
        response = super(ServiceFormMixin, self).form_valid(form)
        return response
