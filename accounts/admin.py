from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile

admin.site.register(Profile, UserAdmin)
