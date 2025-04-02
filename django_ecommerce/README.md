# Django E-Commerce Microservices Architecture

This project implements a microservices-based e-commerce platform using Django. It features a segmented customer service architecture that splits customer handling into three distinct services based on customer type, and a split item service architecture that divides item management into specialized services.

## Architecture Overview

The system consists of the following microservices:

### Core Services
- **Gateway Service**: Central entry point that routes requests to the appropriate services
- **Items Router Service**: Routes item-related requests to specialized item services
- **Cart Service**: Handles shopping cart operations
- **Order Service**: Processes and manages orders
- **Paying Service**: Handles payment processing
- **Shipping Service**: Manages shipping and delivery

### Customer Services Architecture
The customer service architecture implements a router pattern with three specialized implementations:

1. **Customer Service Router**:
   - Acts as a centralized router for all customer-related requests
   - Determines customer type and routes to the appropriate service
   - Provides unified customer API endpoint

2. **Guest Customer Service**:
   - Handles anonymous/guest users
   - Uses SQLite database for simple, file-based storage
   - Manages temporary customer sessions

3. **Registered Customer Service**:
   - Handles regular registered customers
   - Uses MySQL database
   - Features email verification
   - Manages customer profiles and addresses

4. **VIP Customer Service**:
   - Handles premium customers
   - Uses MySQL database
   - Implements tiered VIP levels (Bronze, Silver, Gold, Platinum)
   - Manages exclusive benefits and rewards
   - Features loyalty points system

### Items Services Architecture
The items service has been split into specialized services, each handling a specific type of product:

1. **Book Service**:
   - Manages books with specific attributes (ISBN, author, publisher, etc.)
   - Provides book-specific endpoints (search by author, genre, etc.)
   - Uses dedicated MongoDB database for books

2. **Laptop Service**:
   - Manages laptops with specific attributes (CPU, RAM, storage, etc.)
   - Provides laptop-specific endpoints (search by specs, etc.)
   - Uses dedicated MongoDB database for laptops

3. **Mobile Service**:
   - Manages mobile devices with specific attributes (screen size, camera, etc.)
   - Provides mobile-specific endpoints (search by features, etc.)
   - Uses dedicated MongoDB database for mobile devices

4. **Clothes Service**:
   - Manages clothing items with specific attributes (size, material, color, etc.)
   - Provides clothes-specific endpoints (search by style, size, etc.)
   - Uses dedicated MongoDB database for clothes

### Customer Routing Flow

```
                            ┌─────────────────┐
                            │                 │
                            │  Gateway        │
                            │                 │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │                 │
                            │ Customer Router │
                            │                 │
                            └────────┬────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     │               │               │
                     ▼               ▼               ▼
          ┌─────────────────┐┌─────────────────┐┌─────────────────┐
          │Guest Customer   ││Registered       ││VIP Customer     │
          │Service          ││Customer Service ││Service          │
          └─────────────────┘└─────────────────┘└─────────────────┘
                     │               │               │
                     ▼               ▼               ▼
          ┌─────────────────┐┌─────────────────┐┌─────────────────┐
          │SQLite           ││MySQL            ││MySQL            │
          │                 ││                 ││                 │
          └─────────────────┘└─────────────────┘└─────────────────┘
```

### Items Routing Flow

```
                       ┌─────────────────┐
                       │                 │
                       │  Gateway        │
                       │                 │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │                 │
                       │  Items Router   │
                       │                 │
                       └────────┬────────┘
                                │
         ┌──────────────┬───────┼───────────┬────────────┐
         │              │       │           │            │
         ▼              ▼       ▼           ▼            ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│Book Service     ││Laptop Service   ││Mobile Service   ││Clothes Service  │
│                 ││                 ││                 ││                 │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
         │              │       │           │            │
         ▼              ▼       ▼           ▼            ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│MongoDB          ││MongoDB          ││MongoDB          ││MongoDB          │
│(Books)          ││(Laptops)        ││(Mobiles)        ││(Clothes)        │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
```

## Key Features

- **Service Isolation**: Each customer type and item type has its own dedicated service and database
- **Intelligent Routing**: Router services dynamically route requests to appropriate implementations
- **Seamless Transition**: Customers can transition between services (guest → registered → VIP)
- **Specialized Models**: Each service provides domain-specific data models and validation
- **RESTful APIs**: All services expose RESTful APIs for integration
- **Transparent Proxying**: Requests are transparently proxied to the appropriate service

## Database Architecture

- **Guest Customer Service**: SQLite (file-based)
- **Registered Customer Service**: MySQL
- **VIP Customer Service**: MySQL
- **Book Service**: MongoDB
- **Laptop Service**: MongoDB
- **Mobile Service**: MongoDB
- **Clothes Service**: MongoDB
- **Items Router Service**: MongoDB (for fallback and routing)
- **Transaction Services**: PostgreSQL

## Initial Data Fixtures

To facilitate testing and development, the system includes initial fixture data for all services:

1. **Item Services Fixtures**:
   - Sample books with various genres, authors, and prices
   - Sample laptops with different specifications and brands
   - Sample mobile devices with various features and prices
   - Sample clothes with different sizes, styles, and colors

2. **Customer Services Fixtures**:
   - Sample guest customers with shopping history
   - Sample registered customers with profiles and preferences
   - Sample VIP customers with loyalty points and tier information

3. **Transaction Services Fixtures**:
   - Sample carts with items from different services
   - Sample orders with various statuses and delivery options
   - Sample payments with different payment methods
   - Sample shipping records with tracking information

## Shared Database Architecture

The system implements a shared database architecture to optimize resource usage:

1. **Benefits**:
   - **Resource Efficiency**: Multiple services share database instances
   - **Simplified Management**: Fewer database instances to maintain
   - **Consistent Environment**: Services using the same database type share configuration
   - **Domain Separation**: Each service maintains its own schema/collection
   - **Independent Scaling**: Services can scale independently while sharing database resources

2. **Database Organization**:
   - **MySQL Shared Instance**: Used by Registered Customer and VIP Customer services
   - **MongoDB Shared Instance**: Used by all item services (Books, Laptops, Mobiles, Clothes)
   - **PostgreSQL Shared Instance**: Used by transaction services (Cart, Order, Payment, Shipping)

## Running the Services

### Prerequisites
- Docker and Docker Compose
- Python 3.9+

### Setup Steps

1. Clone the repository:
```
git clone <repository-url>
cd django_ecommerce
```

2. Create data directories:
```
mkdir -p django_ecommerce/guest_customer_service/data
```

3. Build and start the services:
```
docker-compose up --build
```

4. Load initial data:
```
# Run the data loading script
./load_initial_data.sh
```

5. Initialize the VIP benefits (one-time setup):
```
# Enter the VIP customer service container
docker exec -it django_ecommerce_vip-customer_1 bash

# Run the initialization script
python init_benefits.py
```

## Accessing the Services

- Gateway (main entry point): http://localhost:8000
- Customer Service Router: http://localhost:8009
- Guest Customer Service: http://localhost:8001
- Register Customer Service: http://localhost:8007
- VIP Customer Service: http://localhost:8008
- Book Service: http://localhost:8010
- Laptop Service: http://localhost:8011
- Mobile Service: http://localhost:8012
- Clothes Service: http://localhost:8013
- Items Router Service: http://localhost:8005

## API Usage

### Customer Service Routing

The gateway routes customer requests to the customer service router, which then determines the appropriate implementation:

```python
# For a guest/anonymous user
requests.get('http://localhost:8000/api/customers/')

# For a registered user
requests.get('http://localhost:8000/api/customers/',
             headers={'X-User-ID': '123', 'X-Customer-Type': 'registered'})

# For a VIP user
requests.get('http://localhost:8000/api/customers/',
             headers={'X-User-ID': '456', 'X-Customer-Type': 'vip'})
```

### Items Service Routing

The gateway routes item requests to the items router service, which then forwards to the appropriate specialized service:

```python
# Get all items (combined from all services)
requests.get('http://localhost:8000/api/items/')

# Get only books
requests.get('http://localhost:8000/api/items/?type=book')

# Get only laptops
requests.get('http://localhost:8000/api/items/?type=laptop')

# Get only mobiles
requests.get('http://localhost:8000/api/items/?type=mobile')

# Get only clothes
requests.get('http://localhost:8000/api/items/?type=clothes')

# Create a new book
requests.post('http://localhost:8000/api/items/',
              json={'name': 'Clean Code', 'type': 'book', 'author': 'Robert Martin', 'isbn': '9780132350884'})

# Create a new clothing item
requests.post('http://localhost:8000/api/items/',
              json={'name': 'Summer T-Shirt', 'type': 'clothes', 'size': 'L', 'color': 'Blue', 'material': 'Cotton'})
```

### Direct Service Access (for development/testing)

You can also directly access specific services:

```python
# Direct to book service
requests.get('http://localhost:8010/api/books/')

# Direct to laptop service
requests.get('http://localhost:8011/api/laptops/')

# Direct to mobile service
requests.get('http://localhost:8012/api/mobiles/')

# Direct to clothes service
requests.get('http://localhost:8013/api/clothes/')

# Direct to guest customer service
requests.get('http://localhost:8009/api/guest-customer/123/')
```

## Architecture Benefits

- **Scalability**: Each service can scale independently based on demand
- **Resilience**: Failure in one service doesn't affect others
- **Performance**: Optimized databases for each domain
- **Development**: Teams can work on different services independently
- **Extensibility**: New customer types or item types can be added without changing the router pattern
- **Specialization**: Each service can implement domain-specific models, validation, and business logic

## License

This project is licensed under the MIT License - see the LICENSE file for details.