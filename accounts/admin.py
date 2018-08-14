from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


class ClientProfileInline(admin.StackedInline):
    model = ClientUser
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class GeneralPracticeProfileInline(admin.StackedInline):
    model = GeneralPracticeUser
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'type')
        field_classes = {''}


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'password', 'groups', 'is_active', 'is_medidata', 'is_client_admin', 'is_practice_manager')


class UserAdmin(BaseUserAdmin):
    inlines = []
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
    )

    def get_queryset(self, request):
        if hasattr(request.user, 'userprofilebase'):
            queryset = request.user.get_query_set_within_organization()
            return queryset
        return super().get_queryset(request)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        else:
            # dynamic user profile form by User type
            self.inlines = []
            if obj.type == CLIENT_USER:
                self.inlines.append(ClientProfileInline)
            elif obj.type == GENERAL_PRACTICE_USER:
                self.inlines.append(GeneralPracticeProfileInline)
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def get_fieldsets(self, request, obj=None):
        self.add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name'),
            }),
        )

        if request.user.is_medidata or request.user.is_superuser:
            # add permission form
            self.fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_medidata',
                                            'is_client_admin', 'is_practice_manager', 'groups')}),
            )
            # add type field form
            self.add_fieldsets = (
                (None, {
                    'classes': ('wide',),
                    'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'type'),
                }),
            )

        if not obj:
            return self.add_fieldsets

        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if request.user.type == CLIENT_USER:
            obj.type = CLIENT_USER
        elif request.user.type == GENERAL_PRACTICE_USER:
            obj.type = GENERAL_PRACTICE_USER
        super(UserAdmin, self).save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
