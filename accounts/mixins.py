from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic.base import ContextMixin

from SIG_SMEHLA.settings import INDEX_URL
from accounts.models import Profile
from services import models


class AnonymousRequiredMixin(View):
    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy(INDEX_URL))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return super(AnonymousRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy(INDEX_URL))


class SameUserMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        logged_user = Profile.objects.get(id=kwargs['pk'])
        if request.user.is_superuser or request.user == logged_user:
            return super(SameUserMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class SuperuserRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.is_superuser:
            return response
        else:
            raise PermissionDenied


class FACRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(FACRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.occupation == 'FAC':
            return response
        else:
            raise PermissionDenied


class BACRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(BACRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.occupation == 'BAC':
            return response
        else:
            raise PermissionDenied


class BDACRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(BDACRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.occupation == 'BDAC':
            return response
        else:
            raise PermissionDenied


class DIRRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(DIRRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.occupation == 'DIR':
            return response
        else:
            raise PermissionDenied


class AdminRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.occupation == 'ADMIN':
            return response
        else:
            raise PermissionDenied


class ServiceOccupationRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        response = super(ServiceOccupationRequiredMixin, self).dispatch(request, *args, **kwargs)
        service = models.Service.objects.get(pk=kwargs.get('pk'))
        print('dispatch')
        if service:
            print('entro')
            if service.status == '1' and request.user.occupation == 'FAC':
                return response
            elif service.status == '2' and request.user.occupation == 'BAC':
                return response
            elif service.status == '3' and request.user.occupation == 'BDAC':
                return response
            elif service.status == '4' and request.user.occupation == 'DIR':
                return response
            else:
                raise PermissionDenied


class NavbarMixin(ContextMixin):
    tab_name = 'init'

    def get_tab_name(self):
        if self.tab_name:
            return self.tab_name
        else:
            return 'init'

    def get_context_data(self, **kwargs):
        context = super(NavbarMixin, self).get_context_data(**kwargs)
        context['tab'] = self.get_tab_name()
        return context


class AjaxableResponseMixin(generic.FormView):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            response
