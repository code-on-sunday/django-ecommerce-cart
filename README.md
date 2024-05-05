# Django REST API for E-Commerce Cart

This is an open-source Django REST API project for managing an e-commerce cart. It provides functionality for user authentication, creating and managing carts, and handling cart items.

This project is developed by me and the Anthropic Claude AI.

## Features

- [x] User authentication with email and password
- [x] JWT token-based authentication
- [x] View cart details (total items, total price, and item details)
- [ ] CRUD operations for products
- [ ] Create and update carts
- [ ] Add and remove items from the cart

## Installation

1. Clone the repository:

```bash
git clone https://github.com/code-on-sunday/django-ecommerce-cart.git
```

2. Navigate to the project directory:

```bash
cd django-ecommerce-cart
```

3. Create a virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Set up the PostgreSQL database:

```bash
docker-compose up -d
```

6. Apply database migrations:

```bash
python manage.py migrate
```

7. Populate the database with sample data:

```bash
python manage.py seed_users
python manage.py seed_products
python manage.py seed_carts
```

This will create the following sample data:

**Users:**

- John Doe (john.doe@example.com)
- Jane Smith (jane.smith@example.com)
- Bob Johnson (bob.johnson@example.com)

**Products:**

- Product 1 (Price: $9.99)
- Product 2 (Price: $19.99)
- Product 3 (Price: $29.99)

**Carts:**
Each user will have a cart with 1-5 random products added to it.

8. Start the development server:

```bash
python manage.py runserver
```

## Usage

The API endpoints are available at `http://localhost:8000/api/`. You can use tools like Postman or cURL to interact with the API.

### Authentication

- `POST /api/login/`: Authenticate a user and obtain a JWT token.

Example with cURL:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "john.doe@example.com", "password": "password1"}' http://localhost:8000/api/login/
```

### Cart

- `GET /api/cart/`: Retrieve the cart details for the authenticated user.

Example with cURL (replace `<token>` with the JWT token obtained from the login endpoint):

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/cart/
```

## Testing

This project includes test cases for the User, Product, Cart, and CartItem models, as well as for the authentication and cart API views. To run the tests, execute the following command:

```bash
python manage.py test api
```
