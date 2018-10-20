from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

from SIG_SMEHLA.settings import DASHBOARD_URL
from accounts import mixins
from . import forms
from .models import Profile


class LoginView(mixins.AnonymousRequiredMixin, generic.FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy(DASHBOARD_URL))


class LogoutView(generic.RedirectView):
    pattern_name = 'services:index'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class DashBoardView(mixins.LoginRequiredMixin, mixins.NavbarMixin):
    template_name = 'accounts/dashboard.html'
    tab_name = 'dashboard'


class ProfileUpdateView(mixins.SameUserMixin, generic.UpdateView):
    model = Profile
    form_class = forms.ProfileUpdateForm
    template_name = 'accounts/profile_update_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile_update', kwargs={'pk': self.object.pk})


class ProfileDetailView(generic.DetailView):
    model = Profile
