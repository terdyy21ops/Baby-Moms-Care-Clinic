from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Notification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'get_account_status', 'last_login', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__role', 'userprofile__account_status')
    actions = ['activate_users', 'deactivate_users']
    
    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'
    
    def get_account_status(self, obj):
        try:
            status = obj.userprofile.account_status
            if status == 'active':
                return '✓ Active'
            return '✗ Deactivated'
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_account_status.short_description = 'Account Status'
    
    def activate_users(self, request, queryset):
        for user in queryset:
            try:
                user.userprofile.account_status = 'active'
                user.userprofile.save()
                user.is_active = True
                user.save()
            except UserProfile.DoesNotExist:
                pass
        self.message_user(request, f'{queryset.count()} users activated successfully.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        for user in queryset:
            if user != request.user:
                try:
                    user.userprofile.account_status = 'deactivated'
                    user.userprofile.save()
                    user.is_active = False
                    user.save()
                except UserProfile.DoesNotExist:
                    pass
        self.message_user(request, f'Selected users deactivated successfully.')
    deactivate_users.short_description = 'Deactivate selected users'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('created_at',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
