from django.contrib import admin
from .models import Listing, Review, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'listing_type', 'location', 'price', 'created_by', 'is_active', 'created_at']
    list_filter = ['listing_type', 'is_active', 'created_at', 'location']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'listing_type')
        }),
        ('Pricing & Location', {
            'fields': ('price', 'location')
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['listing__title', 'reviewer__username', 'comment']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('listing', 'reviewer', 'rating', 'comment')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'check_in_date', 'check_out_date', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'check_in_date']
    search_fields = ['listing__title', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'duration_days']
    list_editable = ['status']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('listing', 'user', 'check_in_date', 'check_out_date', 'number_of_guests')
        }),
        ('Pricing & Status', {
            'fields': ('total_price', 'status')
        }),
        ('Additional Information', {
            'fields': ('special_requests',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'duration_days'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_days(self, obj):
        """Display booking duration in admin"""
        return obj.duration_days()
    duration_days.short_description = 'Duration (days)'
