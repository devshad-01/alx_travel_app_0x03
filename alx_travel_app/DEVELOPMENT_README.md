# ALX Travel App - Development Setup Documentation

## 📋 Project Overview

This is a Django REST API project for a travel application with the following features:

- **Django REST Framework** for API development
- **MySQL** database integration
- **Swagger/OpenAPI** documentation
- **Celery** for background tasks
- **Redis** as message broker- **CORS** support for frontend integration
- **Environment-based configuration**

## 🏗️ Project Structure

```
alx_travel_app/
├── .env                          # Environment variables (not in git)
├── .gitignore                    # Git ignore rules
├── manage.py                     # Django management script
├── run_with_env.sh              # Environment loading script
├── alx_travel_app/              # Main project package
│   ├── __init__.py              # Celery integration
│   ├── celery.py                # Celery configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI application
│   ├── asgi.py                  # ASGI application
│   ├── requirements.txt         # Python dependencies
│   └── listings/                # Listings app
│       ├── models.py            # Data models (Listing, Review)
│       ├── serializers.py       # DRF serializers
│       ├── views.py             # API views and viewsets
│       ├── urls.py              # App URL patterns
│       ├── admin.py             # Django admin configuration
│       ├── tasks.py             # Celery background tasks
│       └── migrations/          # Database migrations
└── README.MD                    # ALX compliance guide
```

## 🔧 Setup Commands Executed

### 1. Project Initialization

```bash
# Project was already scaffolded following ALX structure
mkdir alx_travel_app
cd alx_travel_app
django-admin startproject alx_travel_app .
cd alx_travel_app
python ../manage.py startapp listings
```

### 2. Dependencies Installation

```bash
# Created requirements.txt with latest dependencies
pip install Django>=5.0.0
pip install djangorestframework>=3.14.0
pip install django-cors-headers>=4.3.0
pip install django-filter>=23.0.0
pip install celery>=5.3.0
pip install drf-yasg>=1.21.0
pip install django-environ>=0.11.0
pip install mysqlclient>=2.2.0
pip install redis>=5.0.0
pip install kombu>=5.3.0
```

### 3. Database Setup

```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE alx_travel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Server Testing

```bash
# Start development server
python manage.py runserver
```

## 📁 Files Created/Modified

### Core Configuration Files

#### `alx_travel_app/requirements.txt`

```
Django>=5.0.0
djangorestframework>=3.14.0
django-cors-headers>=4.3.0
django-filter>=23.0.0
celery>=5.3.0
drf-yasg>=1.21.0
django-environ>=0.11.0
mysqlclient>=2.2.0
redis>=5.0.0
kombu>=5.3.0
```

#### `.env` (Environment Variables)

```bash
# Database Configuration
DB_NAME=alx_travel
DB_USER=root
DB_PASSWORD=Qwerty.25
DB_HOST=localhost
DB_PORT=3306

# Django Configuration
SECRET_KEY=django-insecure-wu&jwz29i)rsnbhe#hcsefehk16-=5rr2&3iwto-1nnpqicd%%
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Django Settings (`alx_travel_app/settings.py`)

**Key configurations added:**

1. **Environment Variables Integration**

```python
import environ
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR.parent / '.env')
```

2. **Installed Apps**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    # Local apps
    'alx_travel_app.listings',
]
```

3. **MySQL Database Configuration**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

4. **REST Framework Configuration**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

5. **CORS Configuration**

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True
```

6. **Swagger Configuration**

```python
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    # ... additional settings
}
```

7. **Celery Configuration**

```python
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

### URL Configuration (`alx_travel_app/urls.py`)

**Swagger and API routes:**

```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel App API",
        default_version='v1',
        description="API documentation for ALX Travel App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alx_travel_app.listings.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### Celery Integration (`alx_travel_app/celery.py`)

```python
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
app = Celery('alx_travel_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Models (`alx_travel_app/listings/models.py`)

**Created models:**

- `Listing`: Travel listings with title, description, type, price, location
- `Review`: User reviews with rating and comments

### API Views (`alx_travel_app/listings/views.py`)

**ViewSets created:**

- `ListingViewSet`: CRUD operations for listings with filtering, search, pagination
- `ReviewViewSet`: CRUD operations for reviews
- Custom actions: `add_review`, `reviews`

### Serializers (`alx_travel_app/listings/serializers.py`)

**DRF serializers:**

- `ListingSerializer`: Full listing serialization with nested reviews
- `ListingCreateSerializer`: Simplified creation serializer
- `ReviewSerializer`: Review serialization
- `UserSerializer`: Basic user information

### Celery Tasks (`alx_travel_app/listings/tasks.py`)

**Background tasks:**

- `send_listing_notification`: Email notifications for new listings
- `send_review_notification`: Email notifications for new reviews
- `cleanup_inactive_listings`: Periodic cleanup task

### Admin Interface (`alx_travel_app/listings/admin.py`)

**Admin configurations:**

- `ListingAdmin`: Advanced admin interface with filters, search
- `ReviewAdmin`: Review management interface

## 🚀 API Endpoints

### Swagger Documentation

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

### API Endpoints

- **Listings**: `http://127.0.0.1:8000/api/listings/`

  - `GET /api/listings/` - List all listings (with filtering, search, pagination)
  - `POST /api/listings/` - Create new listing
  - `GET /api/listings/{id}/` - Get specific listing
  - `PUT /api/listings/{id}/` - Update listing
  - `DELETE /api/listings/{id}/` - Delete listing
  - `POST /api/listings/{id}/add_review/` - Add review to listing
  - `GET /api/listings/{id}/reviews/` - Get listing reviews

- **Reviews**: `http://127.0.0.1:8000/api/reviews/`
  - Standard CRUD operations for reviews

### Filtering & Search

- **Filter by**: `listing_type`, `location`, `rating`
- **Search in**: `title`, `description`, `location`
- **Order by**: `created_at`, `price`, `title`

## 🔧 Development Commands

### Database Operations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Reset database
python manage.py flush
```

### Server Management

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 0.0.0.0:8000

# Run with environment variables (if needed)
./run_with_env.sh python manage.py runserver
```

### Celery Operations

```bash
# Start Celery worker
celery -A alx_travel_app worker --loglevel=info

# Start Celery beat (for periodic tasks)
celery -A alx_travel_app beat --loglevel=info

# Monitor Celery
celery -A alx_travel_app flower
```

### Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test alx_travel_app.listings

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🛠️ Environment Setup

### Prerequisites

1. **Python 3.8+**
2. **MySQL Server** running on localhost:3306
3. **Redis Server** running on localhost:6379 (for Celery)
4. **Virtual Environment** (recommended)

### MySQL Setup

```sql
-- Create database
CREATE DATABASE alx_travel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (if needed)
CREATE USER 'alx_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON alx_travel.* TO 'alx_user'@'localhost';
FLUSH PRIVILEGES;
```

### Redis Setup (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## 📝 Environment Variables

Create a `.env` file in the project root with:

```bash
# Database Configuration
DB_NAME=alx_travel
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## 🔒 Security Notes

1. **Never commit `.env` file** to version control
2. **Use strong SECRET_KEY** in production
3. **Set DEBUG=False** in production
4. **Configure proper ALLOWED_HOSTS** for production
5. **Use environment-specific database credentials**
6. **Enable HTTPS** in production
7. **Configure proper CORS settings** for production

## 🚦 Troubleshooting

### Common Issues

1. **MySQL Connection Error**

   ```bash
   # Check MySQL service
   sudo systemctl status mysql

   # Test connection
   mysql -u root -p -e "SHOW DATABASES;"
   ```

2. **Redis Connection Error**

   ```bash
   # Check Redis service
   sudo systemctl status redis-server

   # Test connection
   redis-cli ping
   ```

3. **Environment Variables Not Loading**

   ```bash
   # Check .env file location
   ls -la .env

   # Test environment loading
   python -c "
   import environ
   env = environ.Env()
   environ.Env.read_env('.env')
   print('DB_NAME:', env('DB_NAME'))
   "
   ```

4. **Import Errors**

   ```bash
   # Check PYTHONPATH
   python -c "import sys; print(sys.path)"

   # Verify app structure
   python manage.py check
   ```

### Performance Optimization

1. **Database Indexing**

   - Add indexes to frequently queried fields
   - Use `select_related` and `prefetch_related` for queries

2. **Caching**

   - Implement Redis caching for API responses
   - Use database query caching

3. **API Optimization**
   - Implement proper pagination
   - Use field selection in serializers
   - Add API rate limiting

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Redis Documentation](https://redis.io/documentation)

## 🎯 Next Steps

1. **Add Authentication**

   - JWT authentication
   - User registration/login endpoints
   - Permission classes

2. **Add More Features**

   - File upload for listing images
   - Booking system
   - Payment integration
   - Email notifications

3. **Frontend Integration**

   - React/Vue.js frontend
   - API integration
   - Real-time updates with WebSockets

4. **Production Deployment**
   - Docker containerization
   - CI/CD pipeline
   - AWS/Heroku deployment
   - Production database setup

---

**Last Updated**: June 13, 2025  
**Django Version**: 5.2.3  
**Python Version**: 3.12.x
