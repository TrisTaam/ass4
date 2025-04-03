from django.core.management.base import BaseCommand
import os
import json
from django.conf import settings
from gateway.views import MOCK_USERS, GatewayView

class Command(BaseCommand):
    help = 'Import initial data for the e-commerce system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data import...'))
        
        # Initialize the GatewayView to access its mock_data
        gateway = GatewayView()
        
        # Add more customers
        self.add_customers(gateway)
        
        # Add more products in each category
        self.add_books(gateway)
        self.add_laptops(gateway)
        self.add_mobiles(gateway)
        self.add_clothes(gateway)
        
        # Add cart items for users
        self.add_cart_items(gateway)
        
        # Add order history
        self.add_orders(gateway)
        
        # Add payment methods
        self.add_payment_methods(gateway)
        
        # Add shipping options and addresses
        self.add_shipping_data(gateway)
        
        # Add more users
        self.add_more_users()
        
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
    
    def add_customers(self, gateway):
        self.stdout.write('Adding customers...')
        gateway.mock_data["customers"] = [
            {
                "id": 1, 
                "name": "John Smith", 
                "email": "john@example.com", 
                "phone": "123-456-7890", 
                "address": "123 Main St, City, Country", 
                "type": "registered"
            },
            {
                "id": 2, 
                "name": "Jane Doe", 
                "email": "jane@example.com", 
                "phone": "987-654-3210", 
                "address": "456 Oak Ave, Town, Country", 
                "type": "vip"
            },
            {
                "id": 3, 
                "name": "Alice Johnson", 
                "email": "alice@example.com", 
                "phone": "555-123-4567", 
                "address": "789 Pine St, Village, Country", 
                "type": "registered"
            },
            {
                "id": 4, 
                "name": "Bob Wilson", 
                "email": "bob@example.com", 
                "phone": "222-333-4444", 
                "address": "101 Maple Dr, Suburb, Country", 
                "type": "guest"
            }
        ]
    
    def add_books(self, gateway):
        self.stdout.write('Adding books...')
        gateway.mock_data["books"] = [
            {
                "id": 1, 
                "name": "The Great Novel", 
                "price": 24.99, 
                "description": "A captivating story about adventure and discovery.", 
                "author": "Jane Author", 
                "publisher": "Good Books Publishing", 
                "category": "books",
                "rating": 4.5,
                "image_url": "/static/img/book.jpg"
            },
            {
                "id": 2, 
                "name": "Programming Fundamentals", 
                "price": 39.99, 
                "description": "Learn the basics of programming with this comprehensive guide.", 
                "author": "John Coder", 
                "publisher": "Tech Press", 
                "category": "books",
                "rating": 4.8,
                "image_url": "/static/img/book.jpg"
            },
            {
                "id": 3, 
                "name": "History of the World", 
                "price": 29.99, 
                "description": "An extensive look at world history through the ages.", 
                "author": "Professor Historian", 
                "publisher": "Academic Press", 
                "category": "books",
                "rating": 4.2,
                "image_url": "/static/img/book.jpg"
            },
            {
                "id": 4, 
                "name": "Cooking Masterclass", 
                "price": 19.99, 
                "description": "Become a master chef with these recipes and techniques.", 
                "author": "Chef Supreme", 
                "publisher": "Food & Cuisine Books", 
                "category": "books",
                "rating": 4.7,
                "image_url": "/static/img/book.jpg"
            }
        ]
    
    def add_laptops(self, gateway):
        self.stdout.write('Adding laptops...')
        gateway.mock_data["laptops"] = [
            {
                "id": 1, 
                "name": "UltraBook Pro", 
                "price": 1299.99, 
                "description": "Thin and light laptop for professionals.", 
                "brand": "TechBrand", 
                "processor": "Intel Core i7", 
                "ram": "16GB", 
                "storage": "512GB SSD",
                "category": "laptops",
                "rating": 4.6,
                "image_url": "/static/img/laptop.jpg"
            },
            {
                "id": 2, 
                "name": "Gaming Master 5000", 
                "price": 1999.99, 
                "description": "Ultimate gaming laptop with high-performance graphics.", 
                "brand": "GameTech", 
                "processor": "AMD Ryzen 9", 
                "ram": "32GB", 
                "storage": "1TB SSD",
                "category": "laptops",
                "rating": 4.9,
                "image_url": "/static/img/laptop.jpg"
            },
            {
                "id": 3, 
                "name": "Student Essential", 
                "price": 699.99, 
                "description": "Affordable laptop for students with all necessary features.", 
                "brand": "EduComp", 
                "processor": "Intel Core i5", 
                "ram": "8GB", 
                "storage": "256GB SSD",
                "category": "laptops",
                "rating": 4.3,
                "image_url": "/static/img/laptop.jpg"
            },
            {
                "id": 4, 
                "name": "Business Elite", 
                "price": 1499.99, 
                "description": "Professional laptop for business executives.", 
                "brand": "CorpTech", 
                "processor": "Intel Core i9", 
                "ram": "32GB", 
                "storage": "1TB SSD",
                "category": "laptops",
                "rating": 4.7,
                "image_url": "/static/img/laptop.jpg"
            }
        ]
    
    def add_mobiles(self, gateway):
        self.stdout.write('Adding mobile phones...')
        gateway.mock_data["mobiles"] = [
            {
                "id": 1, 
                "name": "Galaxy X", 
                "price": 899.99, 
                "description": "Flagship smartphone with cutting-edge features.", 
                "brand": "Samsung", 
                "screen_size": "6.7 inches", 
                "camera": "108MP triple camera", 
                "battery": "5000mAh",
                "category": "mobiles",
                "rating": 4.8,
                "image_url": "/static/img/mobile.jpg"
            },
            {
                "id": 2, 
                "name": "iPhone 15", 
                "price": 999.99, 
                "description": "Latest iPhone with advanced camera system.", 
                "brand": "Apple", 
                "screen_size": "6.5 inches", 
                "camera": "48MP dual camera", 
                "battery": "4500mAh",
                "category": "mobiles",
                "rating": 4.9,
                "image_url": "/static/img/mobile.jpg"
            },
            {
                "id": 3, 
                "name": "Value Phone", 
                "price": 299.99, 
                "description": "Affordable smartphone with great features.", 
                "brand": "Xiaomi", 
                "screen_size": "6.3 inches", 
                "camera": "64MP camera", 
                "battery": "5000mAh",
                "category": "mobiles",
                "rating": 4.5,
                "image_url": "/static/img/mobile.jpg"
            },
            {
                "id": 4, 
                "name": "Pixel Pro", 
                "price": 799.99, 
                "description": "Google's flagship phone with the best camera.", 
                "brand": "Google", 
                "screen_size": "6.4 inches", 
                "camera": "50MP camera with advanced AI", 
                "battery": "4800mAh",
                "category": "mobiles",
                "rating": 4.7,
                "image_url": "/static/img/mobile.jpg"
            }
        ]
    
    def add_clothes(self, gateway):
        self.stdout.write('Adding clothes...')
        gateway.mock_data["clothes"] = [
            {
                "id": 1, 
                "name": "Classic T-Shirt", 
                "price": 19.99, 
                "description": "Comfortable cotton t-shirt for everyday wear.", 
                "brand": "Casual Wear", 
                "size": "M", 
                "color": "Black", 
                "material": "100% Cotton",
                "category": "clothes",
                "rating": 4.4,
                "image_url": "/static/img/clothes.jpg"
            },
            {
                "id": 2, 
                "name": "Formal Business Shirt", 
                "price": 49.99, 
                "description": "Professional shirt for business settings.", 
                "brand": "Executive Apparel", 
                "size": "L", 
                "color": "White", 
                "material": "Cotton Blend",
                "category": "clothes",
                "rating": 4.6,
                "image_url": "/static/img/clothes.jpg"
            },
            {
                "id": 3, 
                "name": "Jeans", 
                "price": 39.99, 
                "description": "Classic blue jeans with comfortable fit.", 
                "brand": "Denim Co", 
                "size": "32", 
                "color": "Blue", 
                "material": "Denim",
                "category": "clothes",
                "rating": 4.3,
                "image_url": "/static/img/clothes.jpg"
            },
            {
                "id": 4, 
                "name": "Hooded Sweatshirt", 
                "price": 29.99, 
                "description": "Warm and comfortable hoodie for casual wear.", 
                "brand": "Urban Street", 
                "size": "XL", 
                "color": "Gray", 
                "material": "Cotton Polyester Blend",
                "category": "clothes",
                "rating": 4.7,
                "image_url": "/static/img/clothes.jpg"
            }
        ]
    
    def add_cart_items(self, gateway):
        self.stdout.write('Adding cart items...')
        gateway.mock_data["cart"] = [
            {
                "id": 1, 
                "customer_id": 1, 
                "items": [
                    {"id": 1, "product_id": 1, "product_type": "books", "name": "The Great Novel", "quantity": 2, "price": 24.99, "image_url": "/static/img/book.jpg"},
                    {"id": 2, "product_id": 3, "product_type": "laptops", "name": "Student Essential", "quantity": 1, "price": 699.99, "image_url": "/static/img/laptop.jpg"}
                ], 
                "total": 749.97
            },
            {
                "id": 2, 
                "customer_id": 2, 
                "items": [
                    {"id": 3, "product_id": 2, "product_type": "mobiles", "name": "iPhone 15", "quantity": 1, "price": 999.99, "image_url": "/static/img/mobile.jpg"},
                    {"id": 4, "product_id": 4, "product_type": "clothes", "name": "Hooded Sweatshirt", "quantity": 2, "price": 29.99, "image_url": "/static/img/clothes.jpg"}
                ], 
                "total": 1059.97
            }
        ]
    
    def add_orders(self, gateway):
        self.stdout.write('Adding order history...')
        gateway.mock_data["orders"] = [
            {
                "id": 1,
                "customer_id": 1,
                "order_number": "ORD-2023-001",
                "items": [
                    {"id": 1, "product_id": 1, "product_type": "books", "name": "The Great Novel", "quantity": 1, "price": 24.99, "image_url": "/static/img/book.jpg"},
                    {"id": 2, "product_id": 3, "product_type": "laptops", "name": "Student Essential", "quantity": 1, "price": 699.99, "image_url": "/static/img/laptop.jpg"}
                ],
                "subtotal": 724.98,
                "shipping": 12.99,
                "tax": 36.25,
                "total": 774.22,
                "status": "Delivered",
                "order_date": "2023-03-15T10:30:00Z",
                "delivery_date": "2023-03-18T14:20:00Z",
                "shipping_address": {
                    "first_name": "John",
                    "last_name": "Smith",
                    "address": "123 Main St",
                    "city": "City",
                    "state": "State",
                    "zip": "12345",
                    "country": "Country",
                    "phone": "123-456-7890"
                },
                "payment_method": {
                    "type": "credit",
                    "last_four": "1234",
                    "expiry": "12/25"
                }
            },
            {
                "id": 2,
                "customer_id": 1,
                "order_number": "ORD-2023-002",
                "items": [
                    {"id": 3, "product_id": 2, "product_type": "books", "name": "Programming Fundamentals", "quantity": 1, "price": 39.99, "image_url": "/static/img/book.jpg"},
                    {"id": 4, "product_id": 4, "product_type": "clothes", "name": "Hooded Sweatshirt", "quantity": 1, "price": 29.99, "image_url": "/static/img/clothes.jpg"}
                ],
                "subtotal": 69.98,
                "shipping": 5.99,
                "tax": 3.50,
                "total": 79.47,
                "status": "Processing",
                "order_date": "2023-04-05T15:45:00Z",
                "delivery_date": None,
                "shipping_address": {
                    "first_name": "John",
                    "last_name": "Smith",
                    "address": "123 Main St",
                    "city": "City",
                    "state": "State",
                    "zip": "12345",
                    "country": "Country",
                    "phone": "123-456-7890"
                },
                "payment_method": {
                    "type": "credit",
                    "last_four": "1234",
                    "expiry": "12/25"
                }
            },
            {
                "id": 3,
                "customer_id": 2,
                "order_number": "ORD-2023-003",
                "items": [
                    {"id": 5, "product_id": 2, "product_type": "mobiles", "name": "iPhone 15", "quantity": 1, "price": 999.99, "image_url": "/static/img/mobile.jpg"}
                ],
                "subtotal": 999.99,
                "shipping": 12.99,
                "tax": 50.00,
                "total": 1062.98,
                "status": "Shipped",
                "order_date": "2023-04-01T09:15:00Z",
                "delivery_date": None,
                "shipping_address": {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "address": "456 Oak Ave",
                    "city": "Town",
                    "state": "State",
                    "zip": "67890",
                    "country": "Country",
                    "phone": "987-654-3210"
                },
                "payment_method": {
                    "type": "credit",
                    "last_four": "5678",
                    "expiry": "11/24"
                }
            }
        ]
    
    def add_payment_methods(self, gateway):
        self.stdout.write('Adding payment methods...')
        gateway.mock_data["payments"] = [
            {
                "id": 1,
                "customer_id": 1,
                "type": "credit",
                "provider": "Visa",
                "account_number": "************1234",
                "expiry": "12/25",
                "name": "John Smith",
                "is_default": True
            },
            {
                "id": 2,
                "customer_id": 1,
                "type": "debit",
                "provider": "Mastercard",
                "account_number": "************5678",
                "expiry": "10/24",
                "name": "John Smith",
                "is_default": False
            },
            {
                "id": 3,
                "customer_id": 2,
                "type": "credit",
                "provider": "American Express",
                "account_number": "***********9012",
                "expiry": "11/24",
                "name": "Jane Doe",
                "is_default": True
            }
        ]
    
    def add_shipping_data(self, gateway):
        self.stdout.write('Adding shipping data...')
        gateway.mock_data["shipping"] = [
            {
                "id": 1,
                "customer_id": 1,
                "addresses": [
                    {
                        "id": 1,
                        "type": "Billing",
                        "first_name": "John",
                        "last_name": "Smith",
                        "address": "123 Main St",
                        "city": "City",
                        "state": "State",
                        "zip": "12345",
                        "country": "Country",
                        "phone": "123-456-7890",
                        "is_default": True
                    },
                    {
                        "id": 2,
                        "type": "Shipping",
                        "first_name": "John",
                        "last_name": "Smith",
                        "address": "123 Main St",
                        "city": "City",
                        "state": "State",
                        "zip": "12345",
                        "country": "Country",
                        "phone": "123-456-7890",
                        "is_default": True
                    }
                ],
                "tracking": [
                    {
                        "order_id": 1,
                        "tracking_number": "TRK12345678",
                        "carrier": "FedEx",
                        "status": "Delivered",
                        "estimated_delivery": "2023-03-18T00:00:00Z",
                        "actual_delivery": "2023-03-18T14:20:00Z",
                        "updates": [
                            {"status": "Order Confirmed", "timestamp": "2023-03-15T10:30:00Z"},
                            {"status": "Processing", "timestamp": "2023-03-16T08:45:00Z"},
                            {"status": "Shipped", "timestamp": "2023-03-16T16:30:00Z"},
                            {"status": "Out for Delivery", "timestamp": "2023-03-18T09:15:00Z"},
                            {"status": "Delivered", "timestamp": "2023-03-18T14:20:00Z"}
                        ]
                    },
                    {
                        "order_id": 2,
                        "tracking_number": "TRK98765432",
                        "carrier": "UPS",
                        "status": "Processing",
                        "estimated_delivery": "2023-04-08T00:00:00Z",
                        "actual_delivery": None,
                        "updates": [
                            {"status": "Order Confirmed", "timestamp": "2023-04-05T15:45:00Z"},
                            {"status": "Processing", "timestamp": "2023-04-06T10:20:00Z"}
                        ]
                    }
                ]
            },
            {
                "id": 2,
                "customer_id": 2,
                "addresses": [
                    {
                        "id": 3,
                        "type": "Billing",
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "address": "456 Oak Ave",
                        "city": "Town",
                        "state": "State",
                        "zip": "67890",
                        "country": "Country",
                        "phone": "987-654-3210",
                        "is_default": True
                    },
                    {
                        "id": 4,
                        "type": "Shipping",
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "address": "456 Oak Ave",
                        "city": "Town",
                        "state": "State",
                        "zip": "67890",
                        "country": "Country",
                        "phone": "987-654-3210",
                        "is_default": True
                    }
                ],
                "tracking": [
                    {
                        "order_id": 3,
                        "tracking_number": "TRK24681357",
                        "carrier": "DHL",
                        "status": "Shipped",
                        "estimated_delivery": "2023-04-06T00:00:00Z",
                        "actual_delivery": None,
                        "updates": [
                            {"status": "Order Confirmed", "timestamp": "2023-04-01T09:15:00Z"},
                            {"status": "Processing", "timestamp": "2023-04-02T13:40:00Z"},
                            {"status": "Shipped", "timestamp": "2023-04-03T11:10:00Z"}
                        ]
                    }
                ]
            }
        ]
        
    def add_more_users(self):
        self.stdout.write('Adding more users to MOCK_USERS...')
        # Get a reference to the global MOCK_USERS
        # Add more users - careful not to duplicate existing ones
        existing_usernames = [user["username"] for user in MOCK_USERS]
        
        new_users = [
            {"username": "customer", "password": "customer123", "email": "customer@example.com"},
            {"username": "alice", "password": "alice123", "email": "alice@example.com"},
            {"username": "bob", "password": "bob123", "email": "bob@example.com"},
            {"username": "guest", "password": "guest123", "email": "guest@example.com"}
        ]
        
        for user in new_users:
            if user["username"] not in existing_usernames:
                MOCK_USERS.append(user)
                existing_usernames.append(user["username"]) 