from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile


class LoginForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        widget=forms.TextInput(
            attrs={'autofocus': True, 'class': 'form-control'}
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )


class CreateProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_('Repeat password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'born_date']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'born_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }

    def clean_password2(self):
        # check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))  # Las contraseñas no coinciden
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'born_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'born_date': forms.DateInput(attrs={'class': 'form-control datepicker'})
        }


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
