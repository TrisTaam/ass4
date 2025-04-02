# Item Service Router

## Architecture Overview

This service implements a router pattern for the e-commerce platform's item catalog. Rather than storing item data directly, it acts as a router that forwards requests to specialized item services based on the item type.

```
                   ┌─────────────────┐
                   │                 │
  User ────────►   │  Item Service   │
                   │    (Router)     │
                   │                 │
                   └─────────────────┘
                          │
      ┌───────────┬───────┼───────────┬────────────┐
      │           │       │           │            │
      ▼           ▼       ▼           ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  Book   │ │ Laptop  │ │ Mobile  │ │ Clothes │ │  Other  │
│ Service │ │ Service │ │ Service │ │ Service │ │Services │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
      │           │       │           │            │
      │           │       │           │            │
      └───────────┴───────┼───────────┴────────────┘
                          ▼                          
                    ┌───────────┐                   
                    │  Shared   │                   
                    │ MongoDB   │                   
                    │ Instance  │                   
                    └───────────┘                   
```

## How It Works

1. The Item Service receives a request from the user or the gateway
2. The router identifies the item type:
   - From request parameters for listing operations
   - From the item type field for creation operations
   - By querying each service for update/delete operations
3. The router forwards the request to the appropriate specialized service
4. The specialized service processes the request using the shared database instance
5. The response is returned to the router and then to the client

## API Endpoints

The Item Service provides a unified API for all item types while forwarding to specialized services:

### Main Endpoints

- `GET /api/items/` - List all items (aggregated from all services)
- `GET /api/items/?type=<type>` - List items of a specific type
- `GET /api/items/{id}/` - Get details for a specific item
- `POST /api/items/` - Create a new item (requires 'type' field)
- `PUT /api/items/{id}/` - Update an item
- `DELETE /api/items/{id}/` - Delete an item

### Type-Specific Endpoints

- `GET /api/items/books/` - List all books
- `GET /api/items/laptops/` - List all laptops
- `GET /api/items/mobiles/` - List all mobile devices
- `GET /api/items/clothes/` - List all clothing items

## Services and Database Architecture

All item-related services share a single MongoDB instance while maintaining logical separation:

- **Book Service**: Uses `ecommerce_books` database in the shared MongoDB instance
- **Laptop Service**: Uses `ecommerce_laptops` database in the shared MongoDB instance
- **Mobile Service**: Uses `ecommerce_mobiles` database in the shared MongoDB instance
- **Clothes Service**: Uses `ecommerce_clothes` database in the shared MongoDB instance

Similarly, all customer services share a single MySQL instance, and all transaction services share a single PostgreSQL instance.

## Benefits of This Architecture

1. **Domain Specialization**: Each service can be optimized for its specific domain
2. **Independent Scaling**: Services can be scaled based on their individual needs
3. **Isolated Development**: Teams can work on different services independently
4. **Resilience**: If one service fails, others continue to function
5. **Resource Efficiency**: Sharing database instances reduces infrastructure costs
6. **Simplified Management**: Fewer database instances to maintain and monitor
7. **Consistent Environment**: Services using the same database type share configuration

## Implementation Notes

The Item Service is implemented as a pure router with no data storage of its own. All item data is stored and managed by the specialized services in their respective databases within the shared MongoDB instance. The `Item` model in this service exists only for reference and documentation purposes. 