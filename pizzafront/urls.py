from django.urls import path
from . import views


urlpatterns = [
    path('', views.getOffers),
    path('offers/', views.getOffers),
    path('menu/', views.getPizza, name='menu'),
    path('user/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('cart/<int:user_id>/<int:pizza_id>/add/', views.addToCart, name='addToCart'),
    path('cart/<int:user_id>/', views.cart, name="cart"),
    path('cart/<int:user_id>/delete/<pizza_id>/', views.deleteCartItem, name="deleteCartItem"),
    path('cart/<int:user_id>/cartSum/', views.cartSum, name="cartSum"),
    path('cart/<int:user_id>/count/', views.countCart, name="count")
]
