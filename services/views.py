from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse

from accounts import mixins
from services import mixins as services_mixins
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

    def get_queryset(self):
        return models.Service.objects.all().order_by('id')


class SearchStatusServiceView(mixins.NavbarMixin, mixins.AjaxableResponseMixin):
    template_name = 'services/status_service.html'
    tab_name = 'status'
    form_class = forms.ServiceStatusFrom
    success_url = reverse_lazy('services:status')

    def form_valid(self, form):
        search = form.search_status()
        if self.request.is_ajax():
            data = None
            if search == {}:
                data = {'message': _('There are not request that correspond with that search')}
            else:
                data = search
            return JsonResponse(data)
        return super().form_valid(form)

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
    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})


class ServiceDetailView(services_mixins.ServiceMixin, generic.DetailView):
    pass


class ServiceUpdateView(services_mixins.ServiceMixin, mixins.ServiceOccupationRequiredMixin, generic.UpdateView):
    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})


class ServiceDeleteView(services_mixins.ServiceMixin, mixins.ServiceOccupationRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy('services:tools')


class EntityListView(mixins.LoginRequiredMixin, mixins.AjaxableListResponseMixin):
    model = models.Entity


class EntityCreateView(mixins.LoginRequiredMixin, mixins.AjaxableResponseMixin, generic.CreateView):
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

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        if name:
            return self.model.objects.filter(name__contains=name)
        return super().get_queryset()


class ChangeStatusServiceView(mixins.AjaxableResponseMixin):
    success_url = reverse_lazy('services:tools')

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk', None)
        if pk:
            service = models.Service.objects.get(pk=pk)
            if service.status == '1':
                service.status = '2'
            elif service.status == '2':
                service.status = '3'
            elif service.status == '3':
                service.status = '4'
            elif service.status == '4':
                service.status = '5'
            service.save()
            if request.is_ajax():
                return JsonResponse({'pk': pk, 'status': service.status})
        return HttpResponseRedirect(self.success_url)
