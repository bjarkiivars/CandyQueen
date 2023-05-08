from django.urls import path
from . import views


urlpatterns = [
    path('offers/', views.getOffers),
    path('menu/', views.getPizza, name='menu'),
    path('user/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('menu/addToCart/<int:pizza_id>/<int:user_id>/', views.addToCart, name='addToCart'),
    path('menu/<int:user_id>/cart/', views.cart)
]
