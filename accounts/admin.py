from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile


class ProfileAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('occupation',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Others dates'), {'fields': ('born_date', 'occupation')}),
    )
    list_filter = UserAdmin.list_filter + ('occupation',)


admin.site.register(Profile, ProfileAdmin)
