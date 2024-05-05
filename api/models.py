from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

def seed_users():
    User.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password1"
    )

    User.objects.create(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        password="password2"
    )

    User.objects.create(
        first_name="Bob",
        last_name="Johnson",
        email="bob.johnson@example.com",
        password="password3"
    )

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

def seed_products():
    Product.objects.create(
        name="Product 1",
        description="This is the first product.",
        price=9.99
    )

    Product.objects.create(
        name="Product 2",
        description="This is the second product.",
        price=19.99
    )

    Product.objects.create(
        name="Product 3",
        description="This is the third product.",
        price=29.99
    )

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart (User: {self.user.email})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

from random import randint

def seed_carts():
    users = User.objects.all()
    products = Product.objects.all()

    for user in users:
        cart = Cart.objects.create(user=user)
        for _ in range(randint(1, 5)):
            product = products[randint(0, len(products) - 1)]
            quantity = randint(1, 5)
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)