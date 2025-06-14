from django.contrib import admin
from .models import Listing, Review


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
