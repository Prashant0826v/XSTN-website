from django.contrib import admin
from .models import JoinCommunity, InternshipApplication, ContactMessage


@admin.register(JoinCommunity)
class JoinCommunityAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'position', 'created_at')
    search_fields = ('full_name', 'email', 'position')
    list_filter = ('position', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Application Details', {
            'fields': ('position', 'experience', 'resume', 'cover_letter')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)