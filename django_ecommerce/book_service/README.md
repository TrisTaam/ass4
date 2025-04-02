# Book Service

This microservice is part of the split item services architecture, responsible for managing all book-related operations in the e-commerce platform.

## Architecture Overview

The items functionality has been split into three specialized services:

1. **Book Service** (this service) - Manages books
2. **Laptop Service** - Manages laptops
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

## Book Service Features

- **Book-specific data model**: ISBN, author, publisher, page count, etc.
- **Book-specific validation**: ISBN format validation, etc.
- **Specialized endpoints**: Search by author, genre, ISBN, etc.
- **Dedicated database**: Optimized for book data storage and retrieval

## API Endpoints

The Book Service exposes the following REST API endpoints:

- `GET /api/books/` - List all books
- `POST /api/books/` - Create a new book
- `GET /api/books/{id}/` - Get details of a specific book
- `PUT /api/books/{id}/` - Update a book
- `DELETE /api/books/{id}/` - Delete a book

Additional specialized endpoints:

- `GET /api/books/genres/` - Get list of all book genres
- `GET /api/books/by_author/?author=<name>` - Find books by author
- `GET /api/books/by_isbn/?isbn=<isbn>` - Find book by ISBN
- `GET /api/books/by_genre/?genre=<genre>` - Find books by genre
- `GET /api/books/in_stock/` - Find all books in stock

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

The Book Service runs on port 8010 and depends on a MongoDB database (db-books). It can be started using Docker Compose:

```
docker-compose up book-service
```

## Development

To add additional book-specific features, extend the Book model or add new endpoints to the BookViewSet. 