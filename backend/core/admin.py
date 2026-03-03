from django.contrib import admin
from .models import (
    JoinCommunity, InternshipApplication, ContactMessage, ProposalForm,
    DeveloperApplication, ConsultationRequest, NewsletterSubscription, Testimonial
)


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


@admin.register(ProposalForm)
class ProposalFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project_type', 'is_read', 'created_at']
    list_filter = ['project_type', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'project_type']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} form(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'


@admin.register(DeveloperApplication)
class DeveloperApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'role_interested', 'experience_level', 'status', 'is_read', 'created_at']
    list_filter = ['experience_level', 'status', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'role_interested', 'skills']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_pending', 'mark_as_reviewed', 'mark_as_selected', 'mark_as_rejected']
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Developer Info', {
            'fields': ('role_interested', 'experience_level', 'skills', 'portfolio_url', 'github_url')
        }),
        ('Application', {
            'fields': ('message', 'status', 'is_read')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} application(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} application(s) marked as pending.')
    mark_as_pending.short_description = 'Mark as pending'
    
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} application(s) marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark as reviewed'
    
    def mark_as_selected(self, request, queryset):
        updated = queryset.update(status='selected')
        self.message_user(request, f'{updated} application(s) marked as selected.')
    mark_as_selected.short_description = 'Mark as selected'
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) marked as rejected.')
    mark_as_rejected.short_description = 'Mark as rejected'


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'consultation_type', 'status', 'is_read', 'created_at']
    list_filter = ['consultation_type', 'status', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'consultation_type']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_pending', 'mark_as_scheduled', 'mark_as_completed', 'mark_as_cancelled']
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Consultation Details', {
            'fields': ('consultation_type', 'preferred_date', 'requirement')
        }),
        ('Status', {
            'fields': ('status', 'is_read')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} request(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} request(s) marked as pending.')
    mark_as_pending.short_description = 'Mark as pending'
    
    def mark_as_scheduled(self, request, queryset):
        updated = queryset.update(status='scheduled')
        self.message_user(request, f'{updated} request(s) marked as scheduled.')
    mark_as_scheduled.short_description = 'Mark as scheduled'
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} request(s) marked as completed.')
    mark_as_completed.short_description = 'Mark as completed'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} request(s) marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark as cancelled'


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscription(s) activated.')
    activate_subscriptions.short_description = 'Activate subscriptions'
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscription(s) deactivated.')
    deactivate_subscriptions.short_description = 'Deactivate subscriptions'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['name', 'company', 'email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    actions = ['approve_testimonials', 'reject_testimonials']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'company', 'email')
        }),
        ('Testimonial', {
            'fields': ('rating', 'message')
        }),
        ('Status', {
            'fields': ('is_approved',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} testimonial(s) approved.')
    approve_testimonials.short_description = 'Approve testimonials'
    
    def reject_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} testimonial(s) rejected.')
    reject_testimonials.short_description = 'Reject testimonials'