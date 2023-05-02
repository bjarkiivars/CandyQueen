from django.urls import path
from . import views


urlpatterns = [
    path('', views.say_hello),
    path('menu/', views.getPizza),
    path('user/', views.userLogin)
]