from django.urls import path
from . import views


urlpatterns = [
    path('menu/', views.getPizza),
    path('offers/', views.getOffers)
]