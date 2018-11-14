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
        if _type == 'visa':
            self.model = models.Visa
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.VisaCreateForm
        elif _type == 'passport':
            self.model = models.Passport
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.PassportCreateForm
        elif _type == 'authorization':
            self.model = models.ResidenceAuthorization
            self.template_name = 'services/residence_form.html'
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.ResidenceAuthorizationForm
        elif _type == 'renovation':
            self.model = models.ResidenceRenovation
            self.template_name = 'services/residence_form.html'
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.ResidenceRenovationForm
        elif _type == 'marriage':
            self.model = models.ResidenceMarriage
            self.template_name = 'services/residence_form.html'
            if issubclass(self.__class__, ModelFormMixin):
                self.form_class = forms.ResidenceMarriageForm
        else:
            raise Http404(_('Service type not found'))
        self.extra_context = {'type': _type}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.service_type == 'visa':
            context['entity_form'] = forms.EntityForm
        return context


class ServiceFormMixin(ServiceMixin, ModelFormMixin):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_type = self.service_type
        self.object.client = models.Client.objects.get(pk=self.kwargs.get('pk'))
        response = super(ServiceFormMixin, self).form_valid(form)
        return response
