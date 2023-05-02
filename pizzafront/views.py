from django.shortcuts import render

from pizzafront.models import *
# from django.http import HttpResponse


# Create your views here.
def getPizza(request):
    response = Pizza.objects.all()
    return render(request, 'index.html', {'Pizza': list(response)})

def getOffers(request):
    response = Offer.objects.all()
    return render(request, 'index.html', {'Offer': list(response)})

def validateLogin(request):
    potential_user = User.objects.filter(request.data.email == email)
    if (potential_user):
        pass