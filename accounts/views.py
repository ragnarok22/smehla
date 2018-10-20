from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic

from SIG_SMEHLA.settings import INDEX_URL
from accounts import mixins
from . import forms
from .models import Profile


class LoginView(mixins.AnonymousRequiredMixin, generic.FormView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy(INDEX_URL))


class LogoutView(generic.RedirectView):
    pattern_name = 'services:index'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class DashBoardView(mixins.SuperuserRequiredMixin, mixins.NavbarMixin, generic.TemplateView):
    template_name = 'accounts/dashboard.html'
    tab_name = 'dashboard'


class ProfileCreateView(mixins.SuperuserRequiredMixin, generic.CreateView):
    model = Profile
    form_class = forms.CreateProfileForm

    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail', kwargs={'pk': self.object.pk})


class ProfileUpdateView(mixins.SameUserMixin, generic.UpdateView):
    model = Profile
    form_class = forms.UpdateProfileForm
    template_name = 'accounts/profile_update_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile_update', kwargs={'pk': self.object.pk})


class ProfileDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Profile


class UpdatePasswordView(mixins.SameUserMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    form_class = auth_forms.PasswordChangeForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(UpdatePasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail', kwargs={'pk': self.request.user.pk})
