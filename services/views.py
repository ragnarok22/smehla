from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from accounts import mixins
from services import models, forms
from services import mixins as services_mixins


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
                context['message'] = _('Has no found any request with %(value)s ci') % {'value': value}
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


class ServiceCreateView(services_mixins.ServiceFormMixin, generic.CreateView):
    object: models.Service

    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})

    def get_context_data(self, **kwargs):
        context = super(ServiceCreateView, self).get_context_data(**kwargs)
        context['entity_form'] = forms.EntityForm
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service_type = self.service_type
        self.object.client = models.Client.objects.get(pk=self.kwargs.get('pk'))
        response = super(ServiceCreateView, self).form_valid(form)
        return response


class ServiceDetailView(services_mixins.ServiceMixin, generic.DetailView):
    pass


class ServiceUpdateView(services_mixins.ServiceMixin, mixins.ServiceOccupationRequiredMixin, generic.UpdateView):
    model = models.Service
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_form'] = forms.EntityForm
        return context

    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})


class ServiceDeleteView(services_mixins.ServiceMixin, generic.DeleteView):
    service_type = None
    success_url = reverse_lazy('services:tools')


class EntityListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Entity


class EntityCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Entity
    form_class = forms.EntityForm
    success_url = reverse_lazy('services:entity_list')


class EntityDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Entity


class EntityUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Entity
    form_class = forms.EntityForm

    def get_success_url(self):
        return reverse_lazy('services:entity_detail', kwargs={'pk': self.object.pk})


class EntityDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Entity
    success_url = reverse_lazy('services:entity_list')


class EntitySearchView(mixins.LoginRequiredMixin, mixins.AjaxableListResponseMixin):
    model = models.Entity

    # def get_queryset(self):
    #     name = self.request.GET.get('name', None)
    #     if name:
    #         return self.model.objects.filter(name__contains=name)
    #     return super().get_queryset()


class ResidenceMarriageCreateView(services_mixins.ServiceMixin, generic.CreateView):
    pass
