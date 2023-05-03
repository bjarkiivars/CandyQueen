from django.shortcuts import render

from pizzafront.models import *
# from django.http import HttpResponse


# Create your views here.
def getPizza(request):
    response = Pizza.objects.all()
    return render(request, 'index.html', {'pizza': list(response)})

def getOffers(request):
    response = Offer.objects.all()
    return render(request, 'index.html', {'offer': list(response)})

def userLogin(request):
    return render(request, 'userlogin.html')
