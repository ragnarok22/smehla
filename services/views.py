from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from accounts import mixins
from services import models, forms


class IndexView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/index.html'
    tab_name = 'init'


class AboutView(generic.TemplateView):
    template_name = 'services/about.html'


class ServicesView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/services.html'
    tab_name = 'services'


class ServiceToolsView(mixins.LoginRequiredMixin, mixins.NavbarMixin, generic.ListView):
    tab_name = 'tools'
    template_name = 'services/tools.html'
    model = models.Service
    paginate_by = 5


class SearchStatusServiceView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/status_service.html'
    tab_name = 'status'

    def get_context_data(self, **kwargs):
        context = super(SearchStatusServiceView, self).get_context_data(**kwargs)
        value = self.request.GET.get('search', None)
        if value:
            service = models.Visa.objects.filter(client__ci=value)
            if service:
                services = []
                for s in service:
                    if s.status == s.SERVICE_STATUS[4][0]:
                        services.append(s)
                if services:
                    context['services'] = services
                else:
                    context['message'] = _('Is in progress')
            else:
                context['message'] = _('Has no found any request with %s ci' % value)
            context['value'] = value
        return context


class ClientCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Client
    form_class = forms.ClientForm

    def get_success_url(self):
        return reverse_lazy('services:client_detail', kwargs={'pk': self.object.pk})


class ClientDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Client


class ClientListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['service_type'] = self.kwargs.get('type')
        return context


class ClientUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Client
    form_class = forms.ClientForm

    def get_success_url(self):
        return reverse_lazy('services:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Client
    success_url = reverse_lazy('services:client_list')


class ServiceCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    object: models.Service
    service_type = None

    def dispatch(self, request, *args, **kwargs):
        _type = kwargs.get('type')
        self.service_type = _type
        if _type == 'visa':
            self.model = models.Visa
            self.form_class = forms.VisaCreateForm
            self.extra_context = {'type': 'visa'}
        elif _type == 'passport':
            self.model = models.Passport
            self.form_class = forms.PassportCreateForm
            self.extra_context = {'type': 'passport'}
        else:
            raise Http404(_('Service type not found'))
        return super(ServiceCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_type = self.service_type
        self.object.client = models.Client.objects.get(pk=self.kwargs.get('pk'))
        response = super(ServiceCreateView, self).form_valid(form)
        return response


class ServiceDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        _type = kwargs.get('type')
        if _type == 'visa':
            self.model = models.Visa
        elif _type == 'passport':
            self.model = models.Passport
        else:
            raise Http404(_('Service type not found'))
        self.extra_context = {'type': _type}
        return super(ServiceDetailView, self).dispatch(request, *args, **kwargs)


class ServiceUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Service
    fields = '__all__'
    service_type = None

    def dispatch(self, request, *args, **kwargs):
        _type = kwargs.get('type')
        self.service_type = _type
        if _type == 'visa':
            self.model = models.Visa
        elif _type == 'passport':
            self.model = models.Passport
        else:
            raise Http404(_('Service type not found'))
        return super(ServiceUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('services:visa_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})


class ServiceDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    service_type = None
    success_url = reverse_lazy('services:tools')

    def dispatch(self, request, *args, **kwargs):
        _type = kwargs.get('type')
        if _type == 'visa':
            self.model = models.Visa
        elif _type == 'passport':
            self.model = models.Passport
        else:
            raise Http404(_('Service type not found'))
        return super(ServiceDeleteView, self).dispatch(request, *args, **kwargs)
