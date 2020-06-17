from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    readonly_fields = [ 'created_date', 'modified_date',]

    # list_display = ('email', 'name', 'date_of_birth', 'is_admin')
    list_display = ('email', 'name', 'is_admin', 'created_date', 'modified_date',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('date_of_birth', 'name')}),
        ('Personal info', {'fields': ('name',)}),
        ('Date', {'fields': ('created_date', 'modified_date',)}),
        ('Profile Image', {'fields': ('image',)}),
        ('Profile Message', {'fields': ('message', )}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('email', 'name', 'date_of_birth', 'password1', 'password2')}
            'fields': ('email', 'name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('email', 'name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)