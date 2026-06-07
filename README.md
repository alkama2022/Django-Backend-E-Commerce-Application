<<<<<<< HEAD

# E-commerce-Backend-API

=======

# E-Commerce Backend API

A robust and scalable E-Commerce Backend built with Django and Django REST Framework (DRF). This project provides RESTful APIs for managing products, categories, customers, orders, payments, and authentication.

## Features

- User Authentication & Authorization
  - JWT Authentication
  - User Registration & Login
  - Role-based Permissions

- Product Management
  - Create, Update, Delete Products
  - Product Categories
  - Product Images
  - Inventory Tracking

- Shopping Cart
  - Add Products to Cart
  - Update Cart Items
  - Remove Cart Items

- Order Management
  - Create Orders
  - Order History
  - Order Status Tracking

- Customer Management
  - Customer Profiles
  - Shipping Addresses

- Payment Integration
  - Payment Processing Support
  - Order Payment Status

- API Documentation
  - Swagger/OpenAPI Support

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Swagger/OpenAPI
- Docker (Optional)

## Project Structure

```text
ecommerce_backend/
│
├── accounts/
├── products/
├── categories/
├── carts/
├── orders/
├── payments/
├── customers/
├── config/
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ecommerce-backend.git
cd ecommerce-backend
```

### 2. Create Virtual Environment

```bash
python -m venv myenv
```

Activate the environment:

**Windows**

```bash
myenv\Scripts\activate
```

**Linux / macOS**

```bash
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will be available at:

```text
http://127.0.0.1:8000/
```

## API Endpoints

### Authentication

| Method | Endpoint                 | Description       |
| ------ | ------------------------ | ----------------- |
| POST   | /api/auth/register/      | Register User     |
| POST   | /api/auth/login/         | Login User        |
| POST   | /api/auth/token/refresh/ | Refresh JWT Token |

### Products

| Method | Endpoint            | Description     |
| ------ | ------------------- | --------------- |
| GET    | /api/products/      | List Products   |
| POST   | /api/products/      | Create Product  |
| GET    | /api/products/{id}/ | Product Details |
| PUT    | /api/products/{id}/ | Update Product  |
| DELETE | /api/products/{id}/ | Delete Product  |

### Categories

| Method | Endpoint         | Description     |
| ------ | ---------------- | --------------- |
| GET    | /api/categories/ | List Categories |
| POST   | /api/categories/ | Create Category |

### Orders

| Method | Endpoint          | Description   |
| ------ | ----------------- | ------------- |
| GET    | /api/orders/      | List Orders   |
| POST   | /api/orders/      | Create Order  |
| GET    | /api/orders/{id}/ | Order Details |

## Running Tests

```bash
python manage.py test
```

## API Documentation

Swagger Documentation:

```text
http://127.0.0.1:8000/swagger/
```

Redoc Documentation:

```text
http://127.0.0.1:8000/redoc/
```

## Deployment

Before deployment:

```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

Collect static files:

```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

Alkama Umar Liman

Backend Developer | Django & Django REST Framework

> > > > > > > a5b504c (Initial commit - Django ecommerce backend)
