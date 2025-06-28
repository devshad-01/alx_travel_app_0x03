from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Review, Booking, Payment


class UserSerializer(serializers.ModelSerializer):
    """User serializer for basic user information"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer"""
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'listing', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'reviewer', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    """Listing serializer with nested reviews"""
    created_by = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'listing_type', 'price', 
            'location', 'created_by', 'created_at', 'updated_at', 
            'is_active', 'reviews', 'average_rating', 'review_count'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        """Calculate average rating from reviews"""
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_review_count(self, obj):
        """Get total number of reviews"""
        return obj.reviews.count()


class ListingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating listings"""
    
    class Meta:
        model = Listing
        fields = ['title', 'description', 'listing_type', 'price', 'location']


class BookingSerializer(serializers.ModelSerializer):
    """Booking serializer"""
    user = UserSerializer(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    listing_details = ListingSerializer(source='listing', read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_details', 'user', 'check_in_date', 
            'check_out_date', 'number_of_guests', 'total_price', 'status',
            'special_requests', 'created_at', 'updated_at', 'duration_days'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'duration_days']
    
    def validate(self, data):
        """Validate booking data"""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out:
            if check_out <= check_in:
                raise serializers.ValidationError(
                    "Check-out date must be after check-in date."
                )
            
            # Check if check-in is not in the past
            from django.utils import timezone
            if check_in < timezone.now().date():
                raise serializers.ValidationError(
                    "Check-in date cannot be in the past."
                )
        
        return data


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer"""
    
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'transaction_id', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'transaction_id', 'status', 'created_at', 'updated_at']
