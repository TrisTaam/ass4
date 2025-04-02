# Mobile Service

This microservice is part of the split item services architecture, responsible for managing all mobile device-related operations in the e-commerce platform.

## Architecture Overview

The items functionality has been split into three specialized services:

1. **Book Service** - Manages books
2. **Laptop Service** - Manages laptops
3. **Mobile Service** (this service) - Manages mobile devices

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

## Mobile Service Features

- **Mobile-specific data model**: Screen size, cameras, processor, battery, etc.
- **Mobile-specific validation**: Hardware specifications validation
- **Specialized endpoints**: Search by OS, camera, network type, features, etc.
- **Dedicated database**: Optimized for mobile device data storage and retrieval

## API Endpoints

The Mobile Service exposes the following REST API endpoints:

- `GET /api/mobiles/` - List all mobile devices
- `POST /api/mobiles/` - Create a new mobile device
- `GET /api/mobiles/{id}/` - Get details of a specific mobile device
- `PUT /api/mobiles/{id}/` - Update a mobile device
- `DELETE /api/mobiles/{id}/` - Delete a mobile device

Additional specialized endpoints:

- `GET /api/mobiles/brands/` - Get list of all mobile brands
- `GET /api/mobiles/by_os/?os_type=<os>&os_version=<version>` - Find mobiles by operating system
- `GET /api/mobiles/by_camera/?min_mp=<megapixels>` - Find mobiles by camera megapixels
- `GET /api/mobiles/by_network/?network=<type>` - Find mobiles by network type (4G/5G)
- `GET /api/mobiles/flagship/` - Find flagship mobile devices
- `GET /api/mobiles/budget/?max_price=<price>` - Find budget-friendly mobile devices
- `GET /api/mobiles/with_features/?nfc=<bool>&fingerprint=<bool>&face_recognition=<bool>&wireless_charging=<bool>` - Find mobiles with specific features
- `GET /api/mobiles/in_stock/` - Find all mobile devices in stock

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

The Mobile Service runs on port 8012 and depends on a MongoDB database (db-mobiles). It can be started using Docker Compose:

```
docker-compose up mobile-service
```

## Development

To add additional mobile-specific features, extend the Mobile model or add new endpoints to the MobileViewSet. 