# Inventory Management System API

This is a Backend API for a simple Inventory Management System, built using Django Rest Framework (DRF). The API supports CRUD operations on inventory items, with JWT-based authentication for secure access. The system integrates with PostgreSQL for the database, Redis for caching frequently accessed items, and includes unit tests to ensure functionality. Additionally, a logging system is implemented to help with debugging and monitoring.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Items](#items)
- [Caching with Redis](#caching-with-redis)
- [Logging](#logging)
- [Getting Help](#getting-help)
- [License](#license)

## Features
- **JWT Authentication**: Secure API access with JWT-based authentication.
- **CRUD Operations**: Create, read, update, and delete inventory items.
- **Redis Caching**: Frequently accessed inventory items are cached in Redis for performance optimization.
- **Error Handling**: Proper error handling with meaningful error codes (400, 404, etc.).
- **Logging**: Detailed logging for API usage, errors, and events.
- **Unit Tests**: Unit tests ensure the correctness of API functionality.

## Technology Stack
- **Web Framework**: *Django*
- **API Framework**: *Django REST Framework*
- **Database**: *SQLite (default) / PostgreSQL (optional)*
- **Caching**: *Redis*
- **Authentication**: *JWT (JSON Web Token)*
- **Logging**: *Python's Logging module*
- **Unit Tests**: *Django REST Framework’s Test framework*

## Installation

### Prerequisites
- Python 3.x
- PostgreSQL (optional)
- Docker (optional)
- Redis

### Steps
1. **Clone the repository**:
    ```bash
    git clone https://github.com/asu2sh/ims-api.git
    cd ims-api
    ```

2. **Set up the virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the Database**: 
   - By default, the project uses SQLite, but you can switch to PostgreSQL by setting environment variables in the `.env` file.
   - If using PostgreSQL, ensure the `USE_POSTGRES=True` variable is set in `.env` and the other database credentials are correct.
    
5. **Create a `.env` file**: 
    Set the following environment variables in a `.env` file (if applicable):
    ```plaintext
    # If using PostgreSQL
      USE_POSTGRES=True
      DB_NAME=<postgres-db-name>
      DB_USER=<postgres-db-username>
      DB_PASSWORD=<postgres-db-password>
      DB_HOST=<postgres-db-host>
      DB_PORT=<postgres-db-port>
    ```

6. **Start Redis**:
   - **Important**: Before proceeding, make sure the Redis service is running. If Redis is installed locally, you can start it with:
     ```bash
     redis-server
     ```
   - Alternatively, if you're using Docker, you can start Redis with:
     ```bash
     docker run --name redis -d -p 6379:6379 redis
     ```

7. **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    
8. **Run Unit Tests**:
    ```bash
    python manage.py test
    ```
    
9. **Run the Django server**:
    ```bash
    python manage.py runserver
    ```

10. **Access the Browsable API**: 
  Visit `http://localhost:8000/api/` in your browser to access the list of browsable API endpoints.

## Logging
The system uses Python's logging module to track errors, API usage, and performance metrics.

- **Log Levels**: Logs can be configured to output at different levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- **File Logging**: Logs can be written to a file by modifying the `LOGGING` configuration in Django's `settings.py`.

## Caching with Redis
The system uses Redis to cache frequently accessed inventory items, optimizing performance by reducing the number of database queries. 

- **Cache Settings**: Items retrieved via `GET /items/<item_id>/` are cached for 300 seconds by default.
- **Invalidation**: The cache is automatically invalidated when items are created, updated, or deleted.

## API Endpoints

### Authentication

- **POST** /auth/register/
  - Register User
  - **Body**:
    
    ```json
    {
      "username": "username",
      "email": "user@example.com",
      "password": "yourpassword",
      "password2": "yourpassword",
      "first_name": "firstname",  # optional
      "last_name": "lastname"  # optional
    }
    ```
    
- **POST** /auth/login/
  - Generate JWT
  - **Body**:
    
    ```json
      {
        "email": "user@example.com",
        "password": "yourpassword"
      }
    ```
  
- **POST** /auth/token/refresh/
  - Refresh JWT
  - **Body**:
    
    ```json
    {
      "refresh": "your-refresh-token"
    }
    ```
    
### Items
- **GET** /items/
  - Retrieve all items.

- **GET** /items/<item_id>/
  - Retrieve an item by ID.

- **POST** /items/
  - Create a new item.
  - **Body**:
    
    ```json
    {
      "name": "Item Name",
      "description": "Item Description",
      "quantity": 10
    }
    ```

- **PUT** /items/<item_id>/
  - Update an item by ID.

- **DELETE** /items/<item_id>/
  - Delete an item by ID.

## Getting Help
If you encounter any issues or have questions about the API, feel free to open an issue on the [GitHub repository](https://github.com/asu2sh/ims-api/issues).
You can also check the [Django REST Framework documentation](https://www.django-rest-framework.org/) for more details on API development and usage.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
