import os
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.getOffers),
    path('offers/', views.getOffers),
    path('', views.getOffers, name='root'),
    path('offers/', views.getOffers, name='offers'),
    path('menu/', views.getPizza, name='menu'),
    path('user/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),
    path('cart/<int:user_id>/<int:pizza_id>/add/', views.addToCart, name='addToCart'),
    path('cart/<int:user_id>/<int:offer_id>/addOffer/', views.addOfferToCart, name='addOfferToCart'),
    path('cart/<int:user_id>/', views.cart, name="cart"),
    path('cart/<int:user_id>/delete/<pizza_id>/', views.deleteCartItem, name="deleteCartItem"),
    path('cart/<int:user_id>/cartSum/', views.cartSum, name="cartSum"),
    path('cart/<int:user_id>/count/', views.countCart, name="count"),
    path('cart/<int:user_id>/offers/<int:offer_id>/', views.getPizzasInOffer, name="getPizzasInOffer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)