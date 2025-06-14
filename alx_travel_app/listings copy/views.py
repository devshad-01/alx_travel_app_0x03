from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Listing, Review
from .serializers import (
    ListingSerializer, 
    ListingCreateSerializer, 
    ReviewSerializer
)


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing travel listings.
    
    Provides CRUD operations for listings with filtering, searching, and ordering.
    """
    queryset = Listing.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['listing_type', 'location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return ListingCreateSerializer
        return ListingSerializer
    
    def perform_create(self, serializer):
        """Set the creator when creating a listing"""
        serializer.save(created_by=self.request.user)
    
    @swagger_auto_schema(
        method='post',
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer, 400: 'Bad Request'}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        """Add a review to a listing"""
        listing = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if user already reviewed this listing
            if Review.objects.filter(listing=listing, reviewer=request.user).exists():
                return Response(
                    {'error': 'You have already reviewed this listing'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(listing=listing, reviewer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={200: ReviewSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a listing"""
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    
    Users can only modify their own reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['listing', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter reviews based on user permissions"""
        if self.action in ['update', 'partial_update', 'destroy']:
            # Users can only modify their own reviews
            return Review.objects.filter(reviewer=self.request.user)
        return Review.objects.all()
    
    def perform_create(self, serializer):
        """Set the reviewer when creating a review"""
        serializer.save(reviewer=self.request.user)
