from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pizzafront.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from django.urls import reverse

from .forms import RegisterForm


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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print("Form data:", request.POST)  # DEBUG: Print form data
        if form.is_valid():
            user = form.save()  # DEBUG: Save the user instance to the database
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect(reverse('login'))
        else:
            print("Form errors:", form.errors)  # DEBUG: Print form errors if it's not valid
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


'''userlogin: IN DEVELOPMENT'''


def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # return redirect('menu')
            return redirect(reverse('menu'))
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

    # Count the amount of items in the cart
    numOfCartItems = 0

    for item in cart:
        numOfCartItems += item.pizza.count()

    context = {
        'cart': cart,
        'num_items': numOfCartItems
    }

    return render(request, 'index.html', context)


def deleteCartItem(request, user_id, pizza_id):
    try:
        # Get the Cart for this user, or throw not found
        cart = get_object_or_404(Cart, user_id=user_id)
        # Get the specific pizza, or throw not found
        pizza = get_object_or_404(Pizza, id=pizza_id)
        # remove the pizza from the cart
        cart.pizza.remove(pizza)
        # re-calculate the sum
        cart.cart_sum -= pizza.price
        # update changes
        cart.save()
        # return json message
        return JsonResponse({'message': 'Cart item deleted successfully'})
    except Exception as e:
        print(e)
        # indicating server error
        return JsonResponse({'message': 'Error deleting item'}, status=500)


# Return the sum of the cart
def cartSum(request, user_id):
    # Get the Cart for this user, or throw not found
    cart = get_object_or_404(Cart, user_id=user_id)

    totalAmount = cart.cart_sum

    return JsonResponse({'totalAmount': totalAmount}, status=200)


# Return the amount of items currently in the cart
def countCart(request, user_id):
    # Get the cart for this user, or throw not found
    cart = get_object_or_404(Cart, user_id=user_id)

    item_counter = cart.pizza.count()

    return JsonResponse({'countedItems': item_counter}, status=200)
