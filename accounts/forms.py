from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from accounts.models import Profile


class LoginForm(AuthenticationForm):
    username = UsernameField(
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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'born_date']
        widgets = {
            'born_date': forms.DateInput(attrs={'class': 'datepicker'})
        }
