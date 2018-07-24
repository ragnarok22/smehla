from django import forms

from account.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'born_date']
        widgets = {
            'born_date': forms.DateInput(attrs={'class': 'datepicker'})
        }
