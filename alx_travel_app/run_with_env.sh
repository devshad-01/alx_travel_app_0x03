#!/bin/bash

# Load environment variables from .env file
export SECRET_KEY="django-insecure-wu&jwz29i)rsnbhe#hcsefehk16-=5rr2&3iwto-1nnpqicd%%"
export DEBUG=True
export ALLOWED_HOSTS="localhost,127.0.0.1"
export DB_NAME="alx_travel"
export DB_USER="root"
export DB_PASSWORD="Qwerty.25"
export DB_HOST="localhost"
export DB_PORT="3306"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# Execute the command passed as arguments
exec "$@"
