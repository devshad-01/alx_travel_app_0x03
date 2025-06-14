from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Listing, Review


@shared_task
def send_listing_notification(listing_id):
    """Send notification when a new listing is created"""
    try:
        listing = Listing.objects.get(id=listing_id)
        subject = f"New Listing Created: {listing.title}"
        message = f"""
        A new listing has been created:
        
        Title: {listing.title}
        Type: {listing.get_listing_type_display()}
        Location: {listing.location}
        Price: ${listing.price}
        
        Created by: {listing.created_by.username}
        """
        
        # In a real application, you would have a list of admin emails
        recipient_list = ['admin@alxtravel.local']  # Replace with actual admin emails
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        
        return f"Notification sent for listing: {listing.title}"
    except Listing.DoesNotExist:
        return f"Listing with id {listing_id} does not exist"


@shared_task
def send_review_notification(review_id):
    """Send notification when a new review is added"""
    try:
        review = Review.objects.get(id=review_id)
        listing = review.listing
        
        subject = f"New Review for {listing.title}"
        message = f"""
        A new review has been added to your listing:
        
        Listing: {listing.title}
        Reviewer: {review.reviewer.username}
        Rating: {review.rating}/5 stars
        Comment: {review.comment}
        """
        
        # Send notification to listing owner
        recipient_list = [listing.created_by.email]
        
        if listing.created_by.email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
        
        return f"Review notification sent for listing: {listing.title}"
    except Review.DoesNotExist:
        return f"Review with id {review_id} does not exist"


@shared_task
def cleanup_inactive_listings():
    """Clean up listings that have been inactive for a long time"""
    from datetime import datetime, timedelta
    
    # Find listings that haven't been updated in 30 days and are marked inactive
    cutoff_date = datetime.now() - timedelta(days=30)
    inactive_listings = Listing.objects.filter(
        is_active=False,
        updated_at__lt=cutoff_date
    )
    
    count = inactive_listings.count()
    # In a real application, you might archive instead of delete
    # inactive_listings.delete()
    
    return f"Found {count} inactive listings for cleanup"
