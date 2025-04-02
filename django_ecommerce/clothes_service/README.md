# Clothes Service

This microservice is part of the split item services architecture, responsible for managing all clothing-related operations in the e-commerce platform.

## Architecture Overview

The items functionality has been split into specialized services:

1. **Book Service** - Manages books
2. **Laptop Service** - Manages laptops
3. **Mobile Service** - Manages mobile devices
4. **Clothes Service** (this service) - Manages clothing items

Each service has its own dedicated MongoDB database:

- Book Service → db-books (MongoDB)
- Laptop Service → db-laptops (MongoDB)
- Mobile Service → db-mobiles (MongoDB)
- Clothes Service → db-clothes (MongoDB)

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
        ┌───────────────┬───────┼───────────────┬───────────────┐
        │               │       │               │               │
        ▼               ▼       ▼               ▼               ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│Book Service     ││Laptop Service   ││Mobile Service   ││Clothes Service  │
│                 ││                 ││                 ││                 │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
        │               │       │               │               │
        ▼               ▼       ▼               ▼               ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│MongoDB          ││MongoDB          ││MongoDB          ││MongoDB          │
│(Books)          ││(Laptops)        ││(Mobiles)        ││(Clothes)        │
└─────────────────┘└─────────────────┘└─────────────────┘└─────────────────┘
```

## Clothes Service Features

- **Clothing-specific data model**: Gender, sizes, materials, colors, etc.
- **Clothing-specific validation**: Material composition, size/color stock validation
- **Specialized endpoints**: Search by gender, category, size, color, material, etc.
- **Outfit recommendations**: Suggest complementary items based on selection
- **Dedicated database**: Optimized for clothing data storage and retrieval

## API Endpoints

The Clothes Service exposes the following REST API endpoints:

- `GET /api/clothes/` - List all clothing items
- `POST /api/clothes/` - Create a new clothing item
- `GET /api/clothes/{id}/` - Get details of a specific clothing item
- `PUT /api/clothes/{id}/` - Update a clothing item
- `DELETE /api/clothes/{id}/` - Delete a clothing item

Additional specialized endpoints:

- `GET /api/clothes/brands/` - Get list of all clothing brands
- `GET /api/clothes/by_gender/?gender=<gender>` - Find clothes by gender
- `GET /api/clothes/by_category/?category=<category>` - Find clothes by category
- `GET /api/clothes/by_size/?size=<size>` - Find clothes available in a specific size
- `GET /api/clothes/by_color/?color=<color>` - Find clothes by color
- `GET /api/clothes/by_material/?material=<material>` - Find clothes by material
- `GET /api/clothes/by_season/?season=<season>` - Find clothes by season
- `GET /api/clothes/on_sale/` - Find clothes that are on sale
- `GET /api/clothes/outfit_recommendation/?category=<category>&color=<color>` - Get outfit recommendations
- `GET /api/clothes/in_stock/` - Find all clothing items in stock

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

The Clothes Service runs on port 8013 and depends on a MongoDB database (db-clothes). It can be started using Docker Compose:

```
docker-compose up clothes-service
```

## Development

To add additional clothing-specific features, extend the Clothes model or add new endpoints to the ClothesViewSet. 