from django.urls import reverse_lazy
from django.views import generic

from accounts import mixins
from services import models


class IndexView(mixins.NavbarMixin):
    template_name = 'services/index.html'
    tab_name = 'init'


class ServicesView(mixins.NavbarMixin):
    template_name = 'services/services.html'
    tab_name = 'services'


class ServiceToolsView(mixins.LoginRequiredMixin, mixins.NavbarMixin):
    tab_name = 'tools'
    template_name = 'services/tools.html'


class ClientCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Client
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('services:client_detail', kwargs={'pk': self.object.pk})


class ClientDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Client


class ClientListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Client


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
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('services:visa_detail', kwargs={'pk': self.object.pk})


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
