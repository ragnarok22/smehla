from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin

from accounts import mixins
from services import models, forms


class ServiceMixin(mixins.LoginRequiredMixin, SingleObjectMixin):
    service_type = None

    def dispatch(self, request, *args, **kwargs):
        _type = kwargs.get('type')
        self.service_type = _type
        if _type == 'visa':
            self.model = models.Visa
        elif _type == 'passport':
            self.model = models.Passport
        elif _type == 'residence':
            self.model = models.ResidenceAuthorization
        else:
            raise Http404(_('Service type not found'))
        self.extra_context = {'type': _type}
        return super(ServiceMixin, self).dispatch(request, *args, **kwargs)


class ServiceFormMixin(ServiceMixin, ModelFormMixin):
    def dispatch(self, request, *args, **kwargs):
        _type = kwargs.get('type')
        self.service_type = _type

        if self.service_type == 'visa':
            self.form_class = forms.VisaCreateForm
        elif self.service_type == 'passport':
            self.form_class = forms.PassportCreateForm
        elif self.service_type == 'residence':
            self.form_class = forms.ResidenceForm
        return super(ServiceFormMixin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_type = self.service_type
        self.object.client = models.Client.objects.get(pk=self.kwargs.get('pk'))
        response = super(ServiceFormMixin, self).form_valid(form)
        return response
