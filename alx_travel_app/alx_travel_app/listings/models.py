from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    """Travel listing model for accommodations, activities, etc."""
    
    LISTING_TYPES = [
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('activity', 'Activity'),
        ('restaurant', 'Restaurant'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title


class Review(models.Model):
    """Review model for listings"""
    
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('listing', 'reviewer')
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.reviewer.username} - {self.listing.title} ({self.rating}/5)'
