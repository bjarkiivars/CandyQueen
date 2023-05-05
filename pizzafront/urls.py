from django.urls import path
from . import views


urlpatterns = [
    path('offers/', views.getOffers),
    path('menu/', views.getPizza),
    path('user/', views.userlogin),
    path('register/', views.getPizza, name='register'), # Temporary for TESTING purposes
    path('menu/addToCart/<int:pizza_id>/<int:user_id>/', views.addToCart, name='addToCart'),
    path('menu/<int:user_id>/cart/', views.cart)
]
