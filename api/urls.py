from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('cart/', views.get_cart_details, name='cart'),
]