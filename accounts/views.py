import datetime

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from accounts import mixins
from services.models import Visa
from . import forms
from .models import Profile


class LoginView(mixins.AnonymousRequiredMixin, generic.FormView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            if self.request.user.occupation == 'ADMIN':
                return reverse_lazy('accounts:dashboard')
            else:
                return reverse_lazy('services:tools')


class LogoutView(generic.RedirectView):
    pattern_name = 'services:index'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class DashBoardView(mixins.SuperuserRequiredMixin, mixins.NavbarMixin, generic.ListView):
    template_name = 'accounts/dashboard.html'
    tab_name = 'dashboard'
    model = Profile


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


class ProfileDeleteView(mixins.SuperuserRequiredMixin, generic.DeleteView):
    model = Profile
    success_url = reverse_lazy('accounts:dashboard')


class UpdatePasswordView(mixins.SameUserMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    form_class = forms.PasswordChangeForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(UpdatePasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail', kwargs={'pk': self.request.user.pk})


class PasswordResetView(auth_views.PasswordResetView):
    # Send the email
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:reset_password_done')
    form_class = forms.PasswordResetForm


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    # Show a success message for the above
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    # checks the link the user clicked and prompts for a new password
    pass


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    # shows a success message for the above
    pass


class ChangeActiveUsersView(mixins.SuperuserRequiredMixin, generic.FormView):
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk', None)
        if pk:
            user = Profile.objects.get(pk=pk)
            user.is_active = not user.is_active
            user.save()
            if request.is_ajax():
                return JsonResponse({'active': user.is_active, 'pk': user.pk})

        return HttpResponseRedirect('/')


class SendEmailView(generic.FormView):
    form_class = forms.SendEmailForm
    template_name = 'accounts/send_email.html'
    success_url = reverse_lazy('accounts:send_email')

    def form_valid(self, form):
        form.send_email()
        return super(SendEmailView, self).form_valid(form)
