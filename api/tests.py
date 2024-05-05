from django.test import TestCase
from .models import User, seed_users, Product, seed_products, Cart, CartItem, seed_carts

class UserModelTestCase(TestCase):
    def test_user_model_fields(self):
        """
        This test case verifies that the User model has the expected fields.
        """
        user = User()
        self.assertIsInstance(user.first_name, str)
        self.assertIsInstance(user.last_name, str)
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.password, str)

    def test_user_model_str_representation(self):
        """
        This test case verifies that the __str__ method of the User model returns the expected string representation.
        """
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.assertEqual(str(user), "John Doe (john.doe@example.com)")

class UserSeedTestCase(TestCase):
    def test_seed_users(self):
        """
        This test case verifies that the seed_users function correctly creates users in the database.
        """
        # Assuming you have a seed_users function in your models.py file
        seed_users()

        # Check if users were created
        self.assertTrue(User.objects.exists())
        self.assertEqual(User.objects.count(), 3)  # Assuming you're creating 3 users

class ProductModelTestCase(TestCase):
    def test_product_model_fields(self):
        """
        This test case verifies that the Product model has the expected fields.
        """
        product = Product()
        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.description, str)
        self.assertIsInstance(product.price, float)

class ProductSeedTestCase(TestCase):
    def test_seed_products(self):
        """
        This test case verifies that the seed_products function correctly creates products in the database.
        """
        # Assuming you have a seed_products function in your models.py file
        seed_products()

        # Check if products were created
        self.assertTrue(Product.objects.exists())
        self.assertEqual(Product.objects.count(), 3)  # Assuming you're creating 3 products

class CartModelTestCase(TestCase):
    def test_cart_model_fields(self):
        """
        This test case verifies that the Cart model has the expected fields.
        """
        user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password1"
        )
        product = Product.objects.create(
            name="Product 1",
            description="This is the first product.",
            price=9.99
        )
        cart = Cart.objects.create(user=user)
        cart_item = cart.items.create(product=product, quantity=2)

        self.assertEqual(cart.user, user)
        self.assertIsInstance(cart_item.product, Product)
        self.assertIsInstance(cart_item.quantity, int)

class SeedCartsTestCase(TestCase):
    def test_seed_carts(self):
        """
        This test case verifies that the seed_carts function correctly creates carts and cart items in the database.
        """
        seed_users()
        seed_products()

        # Assuming you have a seed_carts function in your models.py file
        seed_carts()

        # Check if carts were created
        self.assertTrue(Cart.objects.exists())
        self.assertEqual(Cart.objects.count(), User.objects.count())  # Assuming one cart per user

        # Check if cart items were created
        self.assertTrue(CartItem.objects.exists())
        self.assertGreater(CartItem.objects.count(), 0)  # Assuming at least one cart item

from django.test import Client
from django.urls import reverse
import json
from rest_framework.test import APIClient

class LoginViewTestCase(TestCase):
    def setUp(self):
        seed_users()
        self.client = Client()

    def test_login_with_valid_credentials(self):
        """
        Test that a user can log in with valid email and password.
        """
        login_data = {
            'email': 'john.doe@example.com',
            'password': 'password1'
        }
        response = self.client.post(reverse('login'), data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('token', response_data)
        self.assertIn('success', response_data['message'])

    def test_login_with_invalid_credentials(self):
        """
        Test that a user cannot log in with invalid email or password.
        """
        login_data = {
            'email': 'invalid@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Invalid email or password')

from rest_framework import status
from django.contrib.auth import get_user_model

class CartViewTestCase(TestCase):
    def setUp(self):
        seed_users()
        seed_products()
        seed_carts()
        self.client = APIClient()

    def test_get_cart_details_for_authenticated_user(self):
        """
        Test that an authenticated user can retrieve their cart details.
        """
        user = User.objects.first()

        # Authenticate the user and get the token
        login_data = {
            'email': user.email,
            'password': user.password
        }
        response = self.client.post(reverse('login'), data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content)['token']

        # Set the token in the headers and make a request to the protected cart endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertIn('user_name', response_data)
        self.assertIn('total_items', response_data)
        self.assertIn('total_price', response_data)
        self.assertIn('items', response_data)

    def test_get_cart_details_for_unauthenticated_user(self):
        """
        Test that an unauthenticated user cannot retrieve cart details.
        """
        client = Client()  # Create a new client to avoid authentication from the previous test
        response = client.get(reverse('cart'), follow=True)  # Follow redirects
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenAuthenticationTestCase(TestCase):
    def setUp(self):
        seed_users()
        seed_products()
        seed_carts()
        self.client = APIClient()

    def test_token_authentication(self):
        """
        Test that a user can access the protected cart endpoint with a valid token.
        """
        login_data = {
            'email': 'john.doe@example.com',
            'password': 'password1'
        }
        response = self.client.post(reverse('login'), data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content)['token']

        # Set the token in the headers and make a request to the protected cart endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_token(self):
        """
        Test that a user cannot access the protected cart endpoint without a token.
        """
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        """
        Test that a user cannot access the protected cart endpoint with an invalid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)