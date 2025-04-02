# Laptop Service

This microservice is part of the split item services architecture, responsible for managing all laptop-related operations in the e-commerce platform.

## Architecture Overview

The items functionality has been split into three specialized services:

1. **Book Service** - Manages books
2. **Laptop Service** (this service) - Manages laptops
3. **Mobile Service** - Manages mobile devices

Each service has its own dedicated MongoDB database:

- Book Service → db-books (MongoDB)
- Laptop Service → db-laptops (MongoDB)
- Mobile Service → db-mobiles (MongoDB)

The original Items Service now acts as a router, forwarding requests to the appropriate specialized service based on the item type.

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
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
     ┌─────────────────┐┌─────────────────┐┌─────────────────┐
     │Book Service     ││Laptop Service   ││Mobile Service   │
     │                 ││                 ││                 │
     └─────────────────┘└─────────────────┘└─────────────────┘
                │               │               │
                ▼               ▼               ▼
     ┌─────────────────┐┌─────────────────┐┌─────────────────┐
     │MongoDB          ││MongoDB          ││MongoDB          │
     │(Books)          ││(Laptops)        ││(Mobiles)        │
     └─────────────────┘└─────────────────┘└─────────────────┘
```

## Laptop Service Features

- **Laptop-specific data model**: Processor, RAM, storage, screen, battery, etc.
- **Laptop-specific validation**: Hardware compatibility validation
- **Specialized endpoints**: Search by processor, specs, usage type, etc.
- **Dedicated database**: Optimized for laptop data storage and retrieval

## API Endpoints

The Laptop Service exposes the following REST API endpoints:

- `GET /api/laptops/` - List all laptops
- `POST /api/laptops/` - Create a new laptop
- `GET /api/laptops/{id}/` - Get details of a specific laptop
- `PUT /api/laptops/{id}/` - Update a laptop
- `DELETE /api/laptops/{id}/` - Delete a laptop

Additional specialized endpoints:

- `GET /api/laptops/brands/` - Get list of all laptop brands
- `GET /api/laptops/by_processor/?brand=<brand>&model=<model>` - Find laptops by processor
- `GET /api/laptops/by_specs/?min_ram=<gb>&min_storage=<gb>&min_screen=<inches>` - Find laptops by specifications
- `GET /api/laptops/gaming/` - Find laptops suitable for gaming
- `GET /api/laptops/business/` - Find laptops suitable for business
- `GET /api/laptops/in_stock/` - Find all laptops in stock

## How Routing Works

1. Client makes a request to the Gateway Service
2. Gateway forwards the request to the Items Router 
3. Items Router determines the item type:
   - For existing items: Looks up item type in database
   - For new items: Checks the 'type' field in the request
4. Items Router forwards request to the appropriate specialized service
5. Specialized service processes the request and returns a response
6. Items Router forwards the response back to the Gateway
7. Gateway returns the response to the client

## Running the Service

The Laptop Service runs on port 8011 and depends on a MongoDB database (db-laptops). It can be started using Docker Compose:

```
docker-compose up laptop-service
```

## Development

To add additional laptop-specific features, extend the Laptop model or add new endpoints to the LaptopViewSet. 