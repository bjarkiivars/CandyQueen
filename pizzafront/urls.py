import os
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('', views.getOffers),
    path('offers/', views.getOffers),
    path('', views.getOffers, name='root'),
    path('offers/', views.getOffers, name='offers'),
    path('menu/', views.getPizza, name='menu'),
    path('user/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/<int:pizza_id>/add/', views.addToCart, name='addToCart'),
    path('cart/<int:offer_id>/addOffer/', views.addOfferToCart, name='addOfferToCart'),
    path('cart/', views.cart, name="cart"),
    path('cart/delete/<pizza_id>/', views.deleteCartItem, name="deleteCartItem"),
    path('cart/deleteOffer/<offer_id>/', views.deleteOfferItem, name="deleteOfferItem"),
    path('cart/cartSum/', views.cartSum, name="cartSum"),
    path('cart/count/', views.countCart, name="count"),
    path('cart/offers/<int:offer_id>/', views.getPizzasInOffer, name="getPizzasInOffer"),
    path('cart/addToOffer/<offer_id>/', views.addPizzaToOffer, name="addPizzaToOffer"),
    path('cart/empty/', views.deleteWholeCart, name='deleteWholeCart'),
    path('checkout/', views.checkout)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)