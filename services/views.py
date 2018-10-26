from django.urls import reverse_lazy
from django.views import generic

from accounts import mixins
from services import models, forms
from services.models import Visa, Service


class IndexView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/index.html'
    tab_name = 'init'


class AboutView(generic.TemplateView):
    template_name = 'services/about.html'


class ServicesView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/services.html'
    tab_name = 'services'


class ServiceToolsView(mixins.LoginRequiredMixin, mixins.NavbarMixin, generic.TemplateView):
    tab_name = 'tools'
    template_name = 'services/tools.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceToolsView, self).get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context


class SearchStatusServiceView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/status_service.html'
    tab_name = 'status'

    def get_context_data(self, **kwargs):
        context = super(SearchStatusServiceView, self).get_context_data(**kwargs)
        value = self.request.GET.get('search', None)
        service = Visa.objects.none()
        if value:
            try:
                service = Visa.objects.get(client__ci=value)
            except Visa.DoesNotExist:
                pass
        context['service'] = service
        return context


class ClientCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Client
    fields = '__all__'

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
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('services:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Client
    success_url = reverse_lazy('services:client_list')


class VisaCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Visa
    form_class = forms.VisaCreateForm

    def get_success_url(self):
        return reverse_lazy('services:visa_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(VisaCreateView, self).get_context_data(**kwargs)
        context['client'] = models.Client.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = models.Client.objects.get(pk=self.kwargs.get('pk'))
        response = super(VisaCreateView, self).form_valid(form)
        return response


class VisaDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Visa


class VisaListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Visa


class VisaUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Visa
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('services:visa_detail', kwargs={'pk': self.object.pk})


class VisaDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Visa
    success_url = reverse_lazy('services:visa_list')
