from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Review


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
