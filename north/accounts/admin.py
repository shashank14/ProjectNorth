from django.contrib import admin

from .models import NorthUser
# from .models import Profile
# from .models import ActivationProfile
#

class NorthUserAdmin(admin.ModelAdmin):

    list_display = ['email']

    class Meta:
        model = NorthUser


from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#
#
# from .forms import UserAdminCreationForm, UserAdminChangeForm
#
#
# class NorthUserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('username', 'admin')
#     list_filter = ('admin',)
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ()}),
#         ('Permissions', {'fields': ('active','staff','admin')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2')}
#         ),
#     )
#     search_fields = ('username',)
#     ordering = ('username',)
#     filter_horizontal = ()
#
#
#
#
# # class ProfileAdmin(admin.ModelAdmin):
# #     list_display = ['user']
# #
# #     class Meta:
# #         model = Profile
# #
# # class ActivationProfileAdmin(admin.ModelAdmin):
# #     list_display = ['user']
# #
# #     class Meta:
# #         model = ActivationProfile
#
# # Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

admin.site.register(NorthUser,NorthUserAdmin)
# admin.site.register(Profile,ProfileAdmin)
# admin.site.register(ActivationProfile,ActivationProfileAdmin)
