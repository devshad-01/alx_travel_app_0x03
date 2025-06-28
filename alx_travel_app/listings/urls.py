from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PaymentInitiateView, PaymentVerifyView

router = DefaultRouter()
router.register(r'listings', views.ListingViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/initiate/<int:booking_id>/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('payments/verify/<int:booking_id>/', PaymentVerifyView.as_view(), name='payment-verify'),
]
