# Customer Service Router

This service acts as a router between client requests and the appropriate customer service implementation based on customer type:

1. **Guest Customer Service**: For unauthenticated users
2. **Registered Customer Service**: For standard authenticated users 
3. **VIP Customer Service**: For premium users

## Architecture

The customer service implements a router pattern that:

1. Receives requests from the gateway
2. Determines the customer type based on authentication status or explicit type headers
3. Routes the request to the appropriate implementation (Guest, Registered, or VIP)
4. Returns the response from the underlying service

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

## API Endpoints

The customer service router exposes the following endpoints:

- `GET /api/customer/` - List customers (routed based on user authentication)
- `POST /api/customer/` - Create a customer (routed based on user authentication)
- `GET /api/customer/{id}/` - Get customer details (routed based on customer type)
- `PUT /api/customer/{id}/` - Update customer details (routed based on customer type)
- `DELETE /api/customer/{id}/` - Delete a customer (routed based on customer type)

### Direct Service Access

You can also directly access specific customer service implementations:

- Guest: `/api/guest-customer/{id}/`
- Registered: `/api/registered-customer/{id}/`
- VIP: `/api/vip-customer/{id}/`

## Authentication Headers

When making requests via the Gateway, the following headers can be used to influence routing:

- `X-User-ID`: User identifier for authenticated users
- `X-Customer-Type`: Explicitly specifies the customer type (`guest`, `registered`, or `vip`)

## Implementation Details

1. The router determines the appropriate service based on:
   - Headers from the Gateway
   - User authentication status
   - Database lookup of customer type
   
2. Requests are proxied to the appropriate service
3. Responses are returned transparently to the client

## Database

Each customer service implementation uses its own database:

- **Guest Customer**: SQLite
- **Registered Customer**: MySQL
- **VIP Customer**: MySQL 