from django.contrib import admin
from todolist.models import UserProfile,Item
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

# Register your models here.
# admin.site.register(UserProfile)

class UserProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('email', 'qq', 'phone' )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Item)
