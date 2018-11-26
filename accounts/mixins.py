from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View, generic
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin

from SIG_SMEHLA.settings import INDEX_URL
from accounts.models import Profile


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
        try:
            logged_user = Profile.objects.get(id=kwargs['pk'])
        except Profile.DoesNotExist:
            raise Http404(_('Profile not found'))
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


class AdminRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        response = super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.occupation == 'ADMIN':
            return response
        else:
            raise PermissionDenied


class ServiceOccupationRequiredMixin(LoginRequiredMixin, SingleObjectMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object(self.get_queryset()).can_mod(request.user):
            return super(ServiceOccupationRequiredMixin, self).dispatch(request, *args, **kwargs)
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
            return response


class AjaxableListResponseMixin(generic.ListView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.is_ajax():
            ob_list = []
            for o in self.object_list:
                ob_list.append(o.to_dict())
            return JsonResponse(ob_list, safe=False)
        return response
