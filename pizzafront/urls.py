from django.urls import path
from . import views


urlpatterns = [
    path('offers/', views.getOffers),
    path('menu/', views.getPizza),
    path('user/', views.userLogin)
]