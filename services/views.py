import datetime

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from accounts import mixins
from services import mixins as services_mixins
from services import models, forms


class IndexView(mixins.NavbarMixin, generic.TemplateView):
    template_name = 'services/index.html'
    tab_name = 'init'


class ServiceToolsView(mixins.LoginRequiredMixin, mixins.NavbarMixin, generic.ListView):
    tab_name = 'tools'
    template_name = 'services/tools.html'
    model = models.Service

    def get_queryset(self):
        return models.Service.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super(ServiceToolsView, self).get_context_data(**kwargs)
        now = timezone.now().today()
        future_date = now.date() + datetime.timedelta(days=5)
        context['visa_to_expire'] = models.Visa.objects.filter(  # arreglar consulta
            Q(visa_expiration_date__gte=datetime.date(now.year, now.month, now.day)) &
            Q(visa_expiration_date__lte=future_date)
        )
        context['expired_visa'] = models.Visa.objects.filter(
            Q(visa_expiration_date__lt=now)
        )
        listado = []
        visas = models.Visa.objects.all()
        authorization = models.ResidenceAuthorization.objects.all()
        for v in visas:
            data = {
                'full_name': v.client.get_full_name(),
                'work_name': v.client.work_name,
                'profession': v.client.profession,
                'funcion': v.client.funcion,
                'lodging': v.lodging,
            }
            listado.append(data)
        for a in authorization:
            data = {
                'full_name': a.client.get_full_name(),
                'work_name': a.client.work_name,
                'profession': a.client.profession,
                'funcion': a.client.funcion,
                'lodging': '',
            }
            listado.append(data)

        context['visa_list'] = listado
        context['passport_list'] = models.Passport.objects.all()
        return context


class SearchStatusServiceView(mixins.NavbarMixin, mixins.AjaxableResponseMixin):
    template_name = 'services/status_service.html'
    tab_name = 'status'
    form_class = forms.ServiceStatusFrom
    success_url = reverse_lazy('services:status')

    def form_valid(self, form):
        search = form.search_status()
        if self.request.is_ajax():
            if search.get('data', None) == {}:
                if self.request.POST.get('request_type') == 'passport':
                    data = {'message': _('No request made on this Identity card or personal card')}
                else:
                    data = {'message': _('No request made on this Passport number')}
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
    success_url = reverse_lazy('services:tools')


class ServiceCreateView(services_mixins.ServiceFormMixin, generic.CreateView):
    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})

    def form_valid(self, form):
        if issubclass(self.model, models.ExtensionVisa):
            extension = form.save(commit=False)
            visa_no = models.ExtensionVisa.objects.filter(visa_no__exact=extension.visa_no)
            extension_type = extension.extension_type
            cant_extension = len(visa_no)
            if (extension_type == 'STV' or extension_type == 'TV') and cant_extension >= 1:
                form.add_error(None,
                               ValidationError(_('Only can one extension of Temporary stay visa or Tourist Visa!'),
                                               code='invalid'))
                return self.form_invalid(form)
            elif extension_type == 'OV' and cant_extension >= 2:
                form.add_error(None, ValidationError(_('Only can two extension of Ordinary visa!'), code='invalid'))
                return self.form_invalid(form)
        return super().form_valid(form)


class ServiceDetailView(services_mixins.ServiceMixin, generic.DetailView):
    pass


class ServiceUpdateView(services_mixins.ServiceMixin, mixins.ServiceOccupationRequiredMixin, generic.UpdateView):
    def get_success_url(self):
        return reverse_lazy('services:service_detail', kwargs={'pk': self.object.pk, 'type': self.service_type})


class ServiceDeleteView(services_mixins.ServiceMixin, mixins.ServiceOccupationRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy('services:tools')

    def get_template_names(self):
        if issubclass(self.model, models.Visa):
            return 'services/visa_confirm_delete.html'
        else:
            return super().get_template_names()


class ChangeStatusServiceView(generic.RedirectView):
    pattern_name = 'services:tools'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        type_request = kwargs.get('type_request', None)
        if pk and type_request:
            service = models.Service.objects.get(pk=pk)
            if type_request == 'up':
                if service.status == '1':
                    service.status = '2'
                elif service.status == '2':
                    service.status = '3'
                elif service.status == '3':
                    service.status = '4'
                elif service.status == '4':
                    service.status = '5'
            elif type_request == 'denied':
                service.status = '6'
            elif type_request == 'archive':
                service.status = '7'
            else:
                if service.status == '2':
                    service.status = '1'
                elif service.status == '3':
                    service.status = '2'
                elif service.status == '4':
                    service.status = '3'

            service.save()
        return HttpResponseRedirect(reverse_lazy(self.pattern_name))


class DeliveryView(generic.UpdateView):
    form_class = forms.DeliveryForm
    success_url = reverse_lazy('services:tools')
    model = models.Service

    def form_valid(self, form):
        service = form.save(False)
        service.date_to_collected = timezone.now().today()
        service.official_who_delivers = self.request.user
        service.status = '7'
        service.save()
        return super().form_valid(form)
