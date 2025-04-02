#!/bin/bash

# This script loads initial data for all services in the e-commerce platform
# It assumes the databases have been set up and the services have been migrated

echo "Loading initial data for all services..."

# Book Service
echo "Loading data for Book Service..."
cd /app/book_service
python manage.py loaddata book/fixtures/initial_books.json

# Laptop Service
echo "Loading data for Laptop Service..."
cd /app/laptop_service
python manage.py loaddata laptop/fixtures/initial_laptops.json

# Mobile Service
echo "Loading data for Mobile Service..."
cd /app/mobile_service
python manage.py loaddata mobile/fixtures/initial_mobiles.json

# Clothes Service
echo "Loading data for Clothes Service..."
cd /app/clothes_service
python manage.py loaddata clothes/fixtures/initial_clothes.json

# Customer Service
echo "Loading data for Customer Service..."
cd /app/customer_service
python manage.py loaddata customer/fixtures/initial_customers.json

# Register Customer Service
echo "Loading data for Register Customer Service..."
cd /app/register_customer_service
python manage.py loaddata register_customer_service/fixtures/initial_registered_customers.json

# VIP Customer Service
echo "Loading data for VIP Customer Service..."
cd /app/vip_customer_service
python manage.py loaddata vip_customer_service/fixtures/initial_vip_customers.json

# Cart Service
echo "Loading data for Cart Service..."
cd /app/cart_service
python manage.py loaddata cart/fixtures/initial_carts.json

# Order Service
echo "Loading data for Order Service..."
cd /app/order_service
python manage.py loaddata order/fixtures/initial_orders.json

# Paying Service
echo "Loading data for Paying Service..."
cd /app/paying_service
python manage.py loaddata paying/fixtures/initial_payments.json

# Shipping Service
echo "Loading data for Shipping Service..."
cd /app/shipping_service
python manage.py loaddata shipping/fixtures/initial_shipping.json

echo "All initial data has been loaded successfully!" 