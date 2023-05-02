from django.shortcuts import render

from pizzafront.models import *
# from django.http import HttpResponse


# Create your views here.
def say_hello(request):
    return render(request, 'index.html', {'name': 'Test'})


def getPizza(request):
    response = Pizza.objects.all()
    return render(request, 'index.html', {'name': 'Bjarni', 'Pizza': list(response)})

def userLogin(request):
    return render(request, 'userlogin.html')
