from django.shortcuts import render

from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from .models import User, Cart, CartItem, Product
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse({'message': 'Invalid email or password'}, status=400)
        else:
            # Generate a JWT token for the user
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            return JsonResponse({'message': 'Login successful', 'token': token}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_cart_details(request):
    cart = request.user.cart
    cart_items = cart.items.all()

    user_name = f"{request.user.first_name} {request.user.last_name}"
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    cart_details = {
        'user_name': user_name,
        'total_items': total_items,
        'total_price': total_price,
        'items': [
            {
                'name': item.product.name,
                'price': item.product.price,
                'quantity': item.quantity
            }
            for item in cart_items
        ]
    }

    return JsonResponse(cart_details)