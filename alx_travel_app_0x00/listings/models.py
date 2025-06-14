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


class Booking(models.Model):
    """Booking model for listing reservations"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-booking_date']
        
    def __str__(self):
        return f'{self.guest.username} - {self.listing.title} ({self.check_in_date} to {self.check_out_date})'
    
    def clean(self):
        """Validate booking dates"""
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        if self.check_in_date and self.check_out_date:
            if self.check_in_date >= self.check_out_date:
                raise ValidationError("Check-out date must be after check-in date.")
            if self.check_in_date < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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
