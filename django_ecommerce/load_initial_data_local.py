#!/usr/bin/env python
import os
import subprocess
import sys

print("Loading initial data for all services...")

# Get the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

services = [
    {
        "name": "Book Service",
        "path": os.path.join(base_dir, "book_service"),
        "fixture": "book/fixtures/initial_books.json"
    },
    {
        "name": "Laptop Service",
        "path": os.path.join(base_dir, "laptop_service"),
        "fixture": "laptop/fixtures/initial_laptops.json"
    },
    {
        "name": "Mobile Service",
        "path": os.path.join(base_dir, "mobile_service"),
        "fixture": "mobile/fixtures/initial_mobiles.json"
    },
    {
        "name": "Clothes Service",
        "path": os.path.join(base_dir, "clothes_service"),
        "fixture": "clothes/fixtures/initial_clothes.json"
    },
    {
        "name": "Customer Service",
        "path": os.path.join(base_dir, "customer_service"),
        "fixture": "customer/fixtures/initial_customers.json"
    },
    {
        "name": "Register Customer Service",
        "path": os.path.join(base_dir, "register_customer_service"),
        "fixture": "register_customer_service/fixtures/initial_registered_customers.json"
    },
    {
        "name": "VIP Customer Service",
        "path": os.path.join(base_dir, "vip_customer_service"),
        "fixture": "vip_customer_service/fixtures/initial_vip_customers.json"
    },
    {
        "name": "Cart Service",
        "path": os.path.join(base_dir, "cart_service"),
        "fixture": "cart/fixtures/initial_carts.json"
    },
    {
        "name": "Order Service",
        "path": os.path.join(base_dir, "order_service"),
        "fixture": "order/fixtures/initial_orders.json"
    },
    {
        "name": "Paying Service",
        "path": os.path.join(base_dir, "paying_service"),
        "fixture": "paying/fixtures/initial_payments.json"
    },
    {
        "name": "Shipping Service",
        "path": os.path.join(base_dir, "shipping_service"),
        "fixture": "shipping/fixtures/initial_shipping.json"
    }
]

for service in services:
    print(f"Loading data for {service['name']}...")
    try:
        os.chdir(service['path'])
        subprocess.run([sys.executable, "manage.py", "loaddata", service['fixture']], check=True)
        print(f"Successfully loaded data for {service['name']}")
    except subprocess.CalledProcessError as e:
        print(f"Error loading data for {service['name']}: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

print("All initial data has been loaded successfully!") 