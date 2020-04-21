from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Contract
from .models import OfficialIdentity

# Register your models here.
admin.site.register(Contract)

# Define an inline admin descriptor for OfficialIdentity model
# which acts a bit like a singleton
class OfficialIdentityInline(admin.StackedInline):
    model = OfficialIdentity
    can_delete = False
    verbose_name_plural = 'officialIdentity'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (OfficialIdentityInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)