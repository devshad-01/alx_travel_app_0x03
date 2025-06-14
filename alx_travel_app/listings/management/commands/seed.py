from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Review, Booking
from decimal import Decimal
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample travel listings, reviews, and bookings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )

    def handle(self, *args, **options):
        listings_count = options['listings']
        users_count = options['users']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting to seed database with {listings_count} listings and {users_count} users...')
        )
        
        # Create users
        users = self.create_users(users_count)
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(users)} users')
        )
        
        # Create listings
        listings = self.create_listings(listings_count, users)
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(listings)} listings')
        )
        
        # Create reviews
        reviews_count = self.create_reviews(listings, users)
        self.stdout.write(
            self.style.SUCCESS(f'Created {reviews_count} reviews')
        )
        
        # Create bookings
        bookings_count = self.create_bookings(listings, users)
        self.stdout.write(
            self.style.SUCCESS(f'Created {bookings_count} bookings')
        )
        
        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            users.append(admin)
        
        # Sample user data
        sample_users = [
            ('john_doe', 'john@example.com', 'John', 'Doe'),
            ('jane_smith', 'jane@example.com', 'Jane', 'Smith'),
            ('bob_wilson', 'bob@example.com', 'Bob', 'Wilson'),
            ('alice_brown', 'alice@example.com', 'Alice', 'Brown'),
            ('charlie_davis', 'charlie@example.com', 'Charlie', 'Davis'),
            ('diana_miller', 'diana@example.com', 'Diana', 'Miller'),
            ('frank_garcia', 'frank@example.com', 'Frank', 'Garcia'),
            ('grace_martinez', 'grace@example.com', 'Grace', 'Martinez'),
            ('henry_lopez', 'henry@example.com', 'Henry', 'Lopez'),
            ('ivy_anderson', 'ivy@example.com', 'Ivy', 'Anderson'),
        ]
        
        for i, (username, email, first_name, last_name) in enumerate(sample_users[:count]):
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name
                )
                users.append(user)
        
        return users

    def create_listings(self, count, users):
        """Create sample listings"""
        listings = []
        
        # Sample listing data
        sample_listings = [
            # Hotels
            ('Luxury Beach Resort', 'Beautiful beachfront resort with stunning ocean views', 'hotel', 250.00, 'Maldives'),
            ('Mountain Lodge Retreat', 'Cozy mountain lodge perfect for hiking enthusiasts', 'hotel', 180.00, 'Swiss Alps'),
            ('City Center Hotel', 'Modern hotel in the heart of downtown', 'hotel', 120.00, 'New York'),
            ('Historic Castle Hotel', 'Stay in a real medieval castle with modern amenities', 'hotel', 300.00, 'Scotland'),
            ('Desert Oasis Resort', 'Luxury resort in the middle of the desert', 'hotel', 220.00, 'Dubai'),
            
            # Apartments
            ('Cozy Studio Apartment', 'Perfect for solo travelers or couples', 'apartment', 80.00, 'Paris'),
            ('Penthouse with City View', 'Luxury penthouse with panoramic city views', 'apartment', 350.00, 'London'),
            ('Beachside Condo', 'Modern condo just steps from the beach', 'apartment', 150.00, 'Miami'),
            ('Historic Loft', 'Converted warehouse loft in artistic district', 'apartment', 130.00, 'Berlin'),
            ('Family Apartment', 'Spacious apartment perfect for families', 'apartment', 110.00, 'Barcelona'),
            
            # Activities
            ('Scuba Diving Adventure', 'Explore coral reefs with certified instructors', 'activity', 85.00, 'Great Barrier Reef'),
            ('Mountain Hiking Tour', 'Guided hiking tour through scenic mountain trails', 'activity', 65.00, 'Colorado'),
            ('Wine Tasting Experience', 'Premium wine tasting in historic vineyards', 'activity', 95.00, 'Tuscany'),
            ('Safari Adventure', 'Wildlife safari with experienced guides', 'activity', 200.00, 'Kenya'),
            ('Northern Lights Tour', 'Guided tour to see the magnificent Aurora Borealis', 'activity', 150.00, 'Iceland'),
            
            # Restaurants
            ('Fine Dining Excellence', 'Michelin-starred restaurant with innovative cuisine', 'restaurant', 120.00, 'Tokyo'),
            ('Traditional Bistro', 'Authentic local cuisine in charming atmosphere', 'restaurant', 45.00, 'Lyon'),
            ('Rooftop Restaurant', 'Dining with spectacular city skyline views', 'restaurant', 75.00, 'Singapore'),
            ('Seaside Seafood Grill', 'Fresh seafood with ocean views', 'restaurant', 60.00, 'Sydney'),
            ('Farm-to-Table Dining', 'Organic ingredients from local farms', 'restaurant', 55.00, 'California'),
        ]
        
        for i in range(min(count, len(sample_listings))):
            title, description, listing_type, price, location = sample_listings[i]
            
            if not Listing.objects.filter(title=title).exists():
                listing = Listing.objects.create(
                    title=title,
                    description=description,
                    listing_type=listing_type,
                    price=Decimal(str(price)),
                    location=location,
                    created_by=random.choice(users),
                    is_active=True
                )
                listings.append(listing)
        
        # Create additional random listings if needed
        if count > len(sample_listings):
            for i in range(len(sample_listings), count):
                listing = Listing.objects.create(
                    title=f'Sample Listing {i+1}',
                    description=f'This is a sample listing for testing purposes. Listing number {i+1}.',
                    listing_type=random.choice(['hotel', 'apartment', 'activity', 'restaurant']),
                    price=Decimal(str(round(random.uniform(50, 500), 2))),
                    location=random.choice(['New York', 'Paris', 'Tokyo', 'London', 'Sydney', 'Rome']),
                    created_by=random.choice(users),
                    is_active=True
                )
                listings.append(listing)
        
        return listings

    def create_reviews(self, listings, users):
        """Create sample reviews"""
        reviews_count = 0
        
        # Sample review comments
        positive_comments = [
            "Amazing experience! Highly recommended.",
            "Perfect location and excellent service.",
            "Beautiful place with stunning views.",
            "Great value for money.",
            "The staff was incredibly friendly and helpful.",
            "Clean, comfortable, and well-maintained.",
            "Exceeded all expectations!",
            "Would definitely stay/visit again.",
        ]
        
        neutral_comments = [
            "Good overall experience.",
            "Nice place, met expectations.",
            "Decent value for the price.",
            "Comfortable and clean.",
            "Standard service, nothing special.",
        ]
        
        negative_comments = [
            "Room was smaller than expected.",
            "Service could be improved.",
            "Overpriced for what you get.",
            "Location was not as advertised.",
            "Had some issues but they were resolved.",
        ]
        
        for listing in listings:
            # Each listing gets 0-5 reviews
            num_reviews = random.randint(0, 5)
            
            # Select random users for reviews (no duplicates per listing)
            available_users = [user for user in users if user != listing.created_by]
            review_users = random.sample(available_users, min(num_reviews, len(available_users)))
            
            for user in review_users:
                rating = random.randint(1, 5)
                
                # Choose comment based on rating
                if rating >= 4:
                    comment = random.choice(positive_comments)
                elif rating == 3:
                    comment = random.choice(neutral_comments)
                else:
                    comment = random.choice(negative_comments)
                
                Review.objects.create(
                    listing=listing,
                    reviewer=user,
                    rating=rating,
                    comment=comment
                )
                reviews_count += 1
        
        return reviews_count

    def create_bookings(self, listings, users):
        """Create sample bookings"""
        bookings_count = 0
        
        # Only create bookings for hotels and apartments
        bookable_listings = [l for l in listings if l.listing_type in ['hotel', 'apartment']]
        
        for listing in bookable_listings:
            # Each listing gets 0-3 bookings
            num_bookings = random.randint(0, 3)
            
            # Select random users for bookings (excluding listing owner)
            available_users = [user for user in users if user != listing.created_by]
            booking_users = random.sample(available_users, min(num_bookings, len(available_users)))
            
            for user in booking_users:
                # Generate random booking dates
                start_date = date.today() + timedelta(days=random.randint(1, 90))
                duration = random.randint(1, 14)  # 1-14 days
                end_date = start_date + timedelta(days=duration)
                
                # Calculate total price (listing price * duration)
                total_price = listing.price * duration
                
                # Random number of guests (1-6)
                guests = random.randint(1, 6)
                
                # Random status
                status = random.choice(['pending', 'confirmed', 'cancelled', 'completed'])
                
                # Special requests (sometimes empty)
                special_requests = ""
                if random.choice([True, False]):
                    requests = [
                        "Late check-in requested",
                        "Ground floor room preferred",
                        "Quiet room please",
                        "Extra towels needed",
                        "Airport pickup required",
                        "Vegetarian breakfast option",
                        "Non-smoking room",
                        "Room with balcony preferred"
                    ]
                    special_requests = random.choice(requests)
                
                Booking.objects.create(
                    listing=listing,
                    user=user,
                    check_in_date=start_date,
                    check_out_date=end_date,
                    number_of_guests=guests,
                    total_price=total_price,
                    status=status,
                    special_requests=special_requests
                )
                bookings_count += 1
        
        return bookings_count
