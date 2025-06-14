# Database Modeling and Data Seeding - ALX Travel App

## 📋 Task Overview

This document outlines the implementation of **Database Modeling and Data Seeding** for the ALX Travel App Django project. The task involved creating comprehensive database models, serializers for API data representation, and a management command to seed the database with sample data.

## 🎯 Objectives Completed

✅ **Database Models**: Created `Listing`, `Review`, and `Booking` models with proper relationships and constraints  
✅ **Serializers**: Implemented DRF serializers for `Listing` and `Booking` models  
✅ **Data Seeding**: Created management command to populate database with sample data  
✅ **API Integration**: Added complete CRUD operations and ViewSets  
✅ **Admin Interface**: Enhanced Django admin for all models

## 🏗️ Database Models Implemented

### 1. Listing Model (`listings/models.py`)

```python
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
```

**Features:**

- Four listing types: hotel, apartment, activity, restaurant
- Price field with decimal precision
- User relationship for listing ownership
- Automatic timestamps
- Active/inactive status

### 2. Review Model (`listings/models.py`)

```python
class Review(models.Model):
    """Review model for listings"""

    RATING_CHOICES = [
        (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'),
        (4, '4 Stars'), (5, '5 Stars'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Features:**

- 1-5 star rating system
- One review per user per listing (unique constraint)
- Optional comment field
- Foreign key relationships to Listing and User

### 3. Booking Model (`listings/models.py`) - **NEW**

```python
class Booking(models.Model):
    """Booking model for travel listings"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Features:**

- Booking status tracking (pending, confirmed, cancelled, completed)
- Date validation with database constraints
- Guest count with minimum validation
- Price tracking and special requests
- Duration calculation method

**Database Constraints:**

```python
constraints = [
    models.CheckConstraint(
        check=models.Q(check_out_date__gt=models.F('check_in_date')),
        name='check_out_after_check_in'
    ),
    models.CheckConstraint(
        check=models.Q(number_of_guests__gte=1),
        name='minimum_one_guest'
    ),
    models.CheckConstraint(
        check=models.Q(total_price__gte=0),
        name='non_negative_price'
    ),
]
```

## 🔄 Serializers Implementation

### 1. ListingSerializer (`listings/serializers.py`)

```python
class ListingSerializer(serializers.ModelSerializer):
    """Listing serializer with nested reviews"""
    created_by = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
```

**Features:**

- Nested user and review data
- Calculated average rating
- Review count aggregation
- Read-only fields for security

### 2. BookingSerializer (`listings/serializers.py`) - **NEW**

```python
class BookingSerializer(serializers.ModelSerializer):
    """Booking serializer"""
    user = UserSerializer(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    listing_details = ListingSerializer(source='listing', read_only=True)
    duration_days = serializers.ReadOnlyField()
```

**Features:**

- Nested user and listing details
- Date validation in serializer
- Duration calculation
- Comprehensive validation for check-in/check-out dates

**Custom Validation:**

```python
def validate(self, data):
    """Validate booking data"""
    check_in = data.get('check_in_date')
    check_out = data.get('check_out_date')

    if check_in and check_out:
        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        if check_in < timezone.now().date():
            raise serializers.ValidationError(
                "Check-in date cannot be in the past."
            )

    return data
```

## 🌱 Data Seeding Implementation

### Management Command (`listings/management/commands/seed.py`)

Created a comprehensive Django management command that seeds the database with realistic sample data:

```bash
python manage.py seed --listings 20 --users 10
```

**Command Features:**

- Configurable number of listings and users
- Creates realistic sample data
- Prevents duplicate data creation
- Creates relationships between models

### Sample Data Generated

#### Users Created:

- **Admin user**: `admin` with superuser privileges
- **Regular users**: john_doe, jane_smith, bob_wilson, alice_brown, etc.
- **Authentication**: All users have password `password123` (admin: `admin123`)

#### Listings Created (20 samples):

- **Hotels**: Luxury Beach Resort, Mountain Lodge Retreat, City Center Hotel
- **Apartments**: Cozy Studio Apartment, Penthouse with City View, Beachside Condo
- **Activities**: Scuba Diving Adventure, Mountain Hiking Tour, Wine Tasting Experience
- **Restaurants**: Fine Dining Excellence, Traditional Bistro, Rooftop Restaurant

#### Reviews Generated:

- **0-5 reviews per listing** with realistic comments
- **Rating-based comments**: Positive (4-5 stars), Neutral (3 stars), Negative (1-2 stars)
- **Sample comments**:
  - Positive: "Amazing experience! Highly recommended."
  - Neutral: "Good overall experience."
  - Negative: "Room was smaller than expected."

#### Bookings Generated:

- **0-3 bookings per bookable listing** (hotels and apartments only)
- **Random date ranges**: 1-90 days in the future, 1-14 day durations
- **Calculated total prices**: listing price × duration
- **Random statuses**: pending, confirmed, cancelled, completed
- **Special requests**: Late check-in, ground floor room, etc.

## 🚀 API Endpoints Added

### Listing Endpoints

- `GET /api/listings/` - List all listings with filtering and search
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Get specific listing
- `PUT/PATCH /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing
- `POST /api/listings/{id}/add_review/` - Add review to listing
- `GET /api/listings/{id}/reviews/` - Get listing reviews

### Booking Endpoints - **NEW**

- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get specific booking
- `PUT/PATCH /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking

### Review Endpoints

- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create new review
- `GET /api/reviews/{id}/` - Get specific review
- `PUT/PATCH /api/reviews/{id}/` - Update review (own reviews only)
- `DELETE /api/reviews/{id}/` - Delete review (own reviews only)

## 🔧 Database Migrations

Created and applied migrations for the new Booking model:

```bash
# Created migrations
python manage.py makemigrations listings

# Applied migrations
python manage.py migrate
```

**Migration files created:**

- `0001_initial.py` - Initial Listing and Review models
- `0002_booking.py` - Added Booking model with constraints

## 👨‍💼 Admin Interface Enhanced

Updated Django admin (`listings/admin.py`) to include Booking model:

```python
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'check_in_date', 'check_out_date', 'status', 'total_price']
    list_filter = ['status', 'check_in_date', 'check_out_date', 'created_at']
    search_fields = ['listing__title', 'user__username', 'special_requests']
    readonly_fields = ['created_at', 'updated_at', 'duration_days']
```

**Admin Features:**

- List view with key booking information
- Filtering by status and dates
- Search across listing titles and usernames
- Readonly calculated fields

## 🛠️ Configuration Updates

### Settings Configuration

Updated `settings.py` app configuration:

```python
INSTALLED_APPS = [
    # ...existing apps...
    'listings',  # Fixed from 'alx_travel_app.listings'
]
```

### URL Configuration

Updated URL routing to include new booking endpoints:

```python
# listings/urls.py
router.register(r'bookings', views.BookingViewSet)

# alx_travel_app/urls.py
path('api/', include('listings.urls')),
```

### Apps Configuration

Fixed app configuration in `listings/apps.py`:

```python
class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'  # Fixed from 'alx_travel_app.listings'
```

## 📊 Testing and Validation

### Seeding Success

```bash
Starting to seed database with 20 listings and 10 users...
Created 10 users
Created 20 listings
Created 42 reviews
Created 23 bookings
Database seeding completed successfully!
```

### Database Verification

The seeded database contains:

- ✅ **10 users** (including admin)
- ✅ **20 listings** across all categories
- ✅ **42 reviews** with realistic ratings and comments
- ✅ **23 bookings** for hotels and apartments only

### API Testing

- ✅ Server starts successfully on `http://127.0.0.1:8000/`
- ✅ API endpoints accessible at `/api/listings/`, `/api/bookings/`, `/api/reviews/`
- ✅ Swagger documentation available at `/swagger/`
- ✅ Django admin interface enhanced with all models

## 🎯 Key Features Implemented

### 1. **Comprehensive Data Modeling**

- Three interconnected models with proper relationships
- Database constraints for data integrity
- Appropriate field types and validations

### 2. **Robust API Serialization**

- Nested serializers for related data
- Custom validation methods
- Calculated fields (average rating, duration)

### 3. **Intelligent Data Seeding**

- Realistic sample data across all models
- Relationship-aware data creation
- Configurable seeding parameters
- Duplicate prevention

### 4. **Full API Integration**

- Complete CRUD operations for all models
- Permission-based access control
- Filtering, searching, and pagination
- Custom actions for reviews

### 5. **Enhanced Admin Interface**

- Comprehensive admin panels for all models
- Advanced filtering and search capabilities
- Readonly calculated fields

## 🚀 Usage Instructions

### 1. **Seed the Database**

```bash
cd /home/shad/Projects/ALX-TRAVEL/alx_travel_app
python manage.py seed --listings 20 --users 10
```

### 2. **Access API Endpoints**

- **Listings API**: `http://127.0.0.1:8000/api/listings/`
- **Bookings API**: `http://127.0.0.1:8000/api/bookings/`
- **Reviews API**: `http://127.0.0.1:8000/api/reviews/`

### 3. **View API Documentation**

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

### 4. **Access Admin Interface**

- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Login**: admin / admin123

### 5. **Run Development Server**

```bash
python manage.py runserver
```

## 📁 Files Created/Modified

### New Files Created:

- `listings/management/__init__.py` - Management package
- `listings/management/commands/__init__.py` - Commands package
- `listings/management/commands/seed.py` - **Data seeding command**
- `listings/migrations/0002_booking.py` - **Booking model migration**

### Files Modified:

- `listings/models.py` - **Added Booking model**
- `listings/serializers.py` - **Added BookingSerializer**
- `listings/views.py` - **Added BookingViewSet**
- `listings/urls.py` - **Added booking endpoints**
- `listings/admin.py` - **Added BookingAdmin**
- `listings/apps.py` - **Fixed app configuration**
- `alx_travel_app/settings.py` - **Fixed INSTALLED_APPS**
- `alx_travel_app/urls.py` - **Updated URL patterns**

## 🔍 Validation Results

### ✅ Requirements Met:

1. **✅ Database Models**: Created Listing, Booking, and Review models with proper relationships and constraints
2. **✅ Serializers**: Implemented serializers for Listing and Booking models with comprehensive validation
3. **✅ Management Command**: Created `seed.py` command that populates database with realistic sample data
4. **✅ Data Seeding**: Successfully tested seeder command and populated database
5. **✅ API Integration**: Full CRUD operations available through Django REST Framework
6. **✅ Admin Interface**: Enhanced Django admin for all models

### 📈 Performance Features:

- Database constraints for data integrity
- Optimized queries with select_related/prefetch_related
- Pagination for large datasets
- Filtering and search capabilities
- Permission-based access control

## 🎉 Summary

Successfully implemented comprehensive database modeling and data seeding for the ALX Travel App with:

- **3 interconnected models** with proper relationships and constraints
- **Complete API serialization** with validation and nested data
- **Intelligent data seeding** with 53 total records across all models
- **Full CRUD operations** through Django REST Framework
- **Enhanced admin interface** for easy data management
- **Comprehensive documentation** and API endpoints

The implementation provides a solid foundation for a travel booking application with proper data modeling, API design, and sample data for testing and development.

---

**Implementation Date**: June 14, 2025  
**Django Version**: 5.2.3  
**Database**: MySQL (alx_travel)  
**Total Records Seeded**: 10 users + 20 listings + 42 reviews + 23 bookings = **95 records**

- **Purpose**: Represents travel accommodations, activities, and restaurants
- **Fields**:
  - `title` - CharField(max_length=200)
  - `description` - TextField
  - `listing_type` - CharField with choices (hotel, apartment, activity, restaurant)
  - `price` - DecimalField(max_digits=10, decimal_places=2)
  - `location` - CharField(max_length=100)
  - `created_by` - ForeignKey to User
  - `created_at` - DateTimeField(auto_now_add=True)
  - `updated_at` - DateTimeField(auto_now=True)
  - `is_active` - BooleanField(default=True)
