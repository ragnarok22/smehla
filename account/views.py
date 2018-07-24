from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

from SIG_SMEHLA.settings import DASHBOARD_URL, LOGIN_URL
from account import mixins
from . import forms
from .models import Profile


class LoginView(mixins.AnonymousRequiredMixin, generic.FormView):
    form_class = AuthenticationForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy(DASHBOARD_URL))


class LogoutView(generic.RedirectView):
    pattern_name = LOGIN_URL
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class DashBoardView(mixins.ProfileMixin, mixins.NavbarMixin):
    template_name = 'account/dashboard.html'


class ProfileUpdateView(generic.UpdateView, mixins.SameUserMixin):
    model = Profile
    form_class = forms.ProfileUpdateForm
    template_name = 'account/profile_update_form.html'

    def get_success_url(self):
        return reverse_lazy('account:profile_update', kwargs={'pk': self.object.pk})


class ProfileDetailView(generic.DetailView):
    model = Profile
