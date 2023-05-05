from django.shortcuts import render, redirect
from django.contrib import messages
from pizzafront.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def getPizza(request):
    pizzas = Pizza.objects.all()
    pizza_type = PizzaType.objects.all()

    # getting all the toppings for each pizza
    pizza_data = []
    for pizza in pizzas:
        toppings = pizza.topping.all()
        pizza_data.append({
            'pizza': pizza,
            'toppings': toppings
        })

    # The data that is sent to the index html
    context = {
        'pizza_data': pizza_data,
        'pizzatype': list(pizza_type)
    }
    # Extracting the human-readable string for pizza types.
    for typeOfPizza in pizza_type:
        typeOfPizza.name_display = typeOfPizza.get_name_display()

    return render(request, 'index.html', context)


def getOffers(request):

    offers = Offer.objects.all()
    pizzas = Pizza.objects.all()
    pizza_type = PizzaType.objects.all()

    # getting all the toppings for each pizza
    pizza_data = []
    for pizza in pizzas:
        toppings = pizza.topping.all()
        pizza_data.append({
            'pizza': pizza,
            'toppings': toppings
        })

    # Extracting the human-readable string for pizza types.
    for typeOfPizza in pizza_type:
        typeOfPizza.name_display = typeOfPizza.get_name_display()

    # The data that is sent to the index html
    context = {
        'offers': list(offers),
        'pizza_data': pizza_data,
        'pizzatype': list(pizza_type)
    }

    return render(request, 'index.html', context)


def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/menu/')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'userlogin.html', {'form': form})


# Add to cart functionality Requires user authentication
# TODO: Finish implementing view, so we can post the cart to the DB
# For now I will force the User in my request to test
def addToCart(request, pizza_id, user_id):
    # retrieve the pizza object from the pizza_id param
    pizza = Pizza.objects.get(id=pizza_id)

    # get the current user
    # TODO: Need to authenticate the user
    # user = request.user
    # Temporary:
    user = User.objects.get(id=user_id)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, cart_sum=0)

    if not cart.pizza.filter(id=pizza.id).exists():
        cart.pizza.add(pizza)

    cart.cart_sum += pizza.price
    cart.save()
    success = 'Added successfully to cart'
    return HttpResponse(success)


def cart(request, user_id):
    user = User.objects.get(id=user_id)

    cart = Cart.objects.filter(user=user).prefetch_related('pizza')

    print(f"cart: {cart}")

    context = {
        'cart': cart
    }

    return render(request, 'index.html', context)