# ALX Django Project Setup Guide

## Required Structure
alx_travel_app/
├── alx_travel_app/ # Main project package
│ ├── listings/ # Your app (inside inner dir)
│ ├── requirements.txt # Dependencies file
│ ├── settings.py
│ └── ...
└── manage.py

text

## Step-by-Step Setup

1. **Scaffold Project**
   ```bash
   mkdir alx_travel_app
   cd alx_travel_app
   django-admin startproject alx_travel_app .
Create Apps Inside Inner Directory

bash
# From project root:
cd alx_travel_app
python ../manage.py startapp listings
cd ..
Set Up Requirements

bash
touch alx_travel_app/requirements.txt
pip freeze > alx_travel_app/requirements.txt
Configure Settings

python
# alx_travel_app/settings.py
INSTALLED_APPS = [
    ...
    'alx_travel_app.listings',
]
Key Commands
Run server (from root):

bash
python manage.py runserver
Make migrations:

bash
python manage.py makemigrations listings
python manage.py migrate
Import Patterns
python
# Within the same app:
from .models import Listing

# From other apps/templates:
from alx_travel_app.listings.models import Listing
ALX Compliance Notes
All app code must live in alx_travel_app/alx_travel_app/

requirements.txt must be inside inner directory

Test paths match exactly:

alx_travel_app/alx_travel_app/listings/views.py

alx_travel_app/alx_travel_app/settings.py

Troubleshooting
If imports fail:

Check __init__.py exists in all packages

Verify all paths use full format: alx_travel_app.listings

Restart VS Code after creating new files

text

**Key Features**:
- Clear visual directory structure
- Copy-paste ready commands
- ALX-specific compliance notes
- Common troubleshooting tips

Place this in your project root as `README.md` and customize the app names as needed. The structure matches exactly what ALX checkers expect.