from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'is_verified', 'is_account_locked_display', 'created_at'
    ]
    
    list_filter = [
        'is_verified', 'created_at', 'email_verified_at',
        'locked_until', 'last_activity',
    ]
    
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'company']
    
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'phone', 'company', 'bio')
        }),
        ('Verification & Security', {
            'fields': (
                'is_verified', 'email_verified_at', 'email_verification_code',
                'email_verification_expires', 'failed_login_attempts', 'locked_until'
            ),
            'classes': ('collapse',)
        }),
        ('Password Reset', {
            'fields': ('password_reset_token', 'password_reset_expires'),
            'classes': ('collapse',)
        }),
        ('Login History', {
            'fields': ('last_login_ip', 'last_login_device', 'last_activity', 'last_login'),
            'classes': ('collapse',)
        }),
        ('Permissions & Groups', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'created_at', 'updated_at', 'email_verified_at', 'last_login',
        'password_reset_token', 'email_verification_code'
    ]
    
    actions = ['unlock_accounts', 'verify_emails', 'reset_failed_attempts']

    def is_account_locked_display(self, obj):
        """Display account lock status with color coding"""
        if obj.is_account_locked():
            return format_html(
                '<span style="color: red;">🔒 Locked</span>'
            )
        return format_html(
            '<span style="color: green;">✓ Active</span>'
        )
    is_account_locked_display.short_description = 'Status'

    def unlock_accounts(self, request, queryset):
        """Admin action to unlock accounts"""
        count = 0
        for user in queryset:
            if user.is_account_locked():
                user.locked_until = None
                user.failed_login_attempts = 0
                user.save()
                count += 1
        self.message_user(request, f'{count} account(s) unlocked.')
    unlock_accounts.short_description = 'Unlock selected accounts'

    def verify_emails(self, request, queryset):
        """Admin action to manually verify emails"""
        count = queryset.filter(is_verified=False).update(
            is_verified=True,
            email_verified_at=timezone.now(),
            email_verification_code=None,
            email_verification_expires=None
        )
        self.message_user(request, f'{count} email(s) verified.')
    verify_emails.short_description = 'Mark emails as verified'

    def reset_failed_attempts(self, request, queryset):
        """Admin action to reset failed login attempts"""
        count = 0
        for user in queryset:
            if user.failed_login_attempts > 0:
                user.reset_failed_login_attempts()
                count += 1
        self.message_user(request, f'{count} user(s) reset.')
    reset_failed_attempts.short_description = 'Reset failed login attempts'

