from django.urls import reverse_lazy
from django.views import generic

from accounts import mixins
from services.models import Client


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
    model = Client
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('services:client_detail', kwargs={'pk': self.object.pk})


class ClientDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Client


class ClientListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Client


class ClientUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Client
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('services:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('services:client_list')
