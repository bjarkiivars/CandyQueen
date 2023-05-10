from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pizzafront.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Prefetch
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


'''
Logs the user in and creates a valid session
TODO: If possible clean the function up / better code
'''


def userlogin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            return redirect(reverse('menu'))
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'userlogin.html', {'form': form})


def userlogout(request):
    logout(request)
    return redirect('menu')


def addOfferToCart(request, offer_id, user_id):
    offer = Offer.objects.get(id=offer_id)

    user = User.objects.get(id=user_id)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, cart_sum=0)

    existing_offer = cart.offer_quantity.filter(offer_name=offer.offer_name).first()

    if existing_offer:
        cart_offer = CartOfferQuantity.objects.get(cart=cart, offer=existing_offer)
        cart_offer.quantity += 1
        cart_offer.save()
    else:
        cart_offer = CartOfferQuantity.objects.create(cart=cart, offer=offer, quantity=1)

    cart.cart_sum += offer.offer_price
    cart.save()
    success = 'Added Offer successfully to cart'
    return HttpResponse(success)


# Add to cart functionality Requires user authentication
# TODO: Finish implementing view, so we can post the cart to the DB
# For now I will force the User in my request to test


#@login_required(login_url='/user/')
def addToCart(request, pizza_id, user_id):

    # Will be used later

    # Check if user can access this feature (is authenticated)
    # if not request.user.is_authenticated:
    #    messages.error(request, 'Login is required for this feature.')
    #    return redirect('login')
    # retrieve the pizza object from the pizza_id param


    pizza = Pizza.objects.get(id=pizza_id)

    # get the current user
    # TODO: Need to authenticate the user
    # Temporary:
    user = User.objects.get(id=user_id)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, cart_sum=0)

    # check if pizza already exists in cart
    existing_pizza = cart.pizza.filter(name=pizza.name, size=pizza.size, topping__in=pizza.topping.all()).first()

    if existing_pizza:
        # if pizza already exists, increment quantity instead of adding a new one
        cart_pizza = CartPizza.objects.get(cart=cart, pizza=existing_pizza)
        cart_pizza.quantity += 1
        cart_pizza.save()
    else:
        # if pizza does not exist, add it to cart with quantity=1
        cart_pizza = CartPizza.objects.create(cart=cart, pizza=pizza, quantity=1)

    cart.cart_sum += pizza.price
    cart.save()
    success = 'Added successfully to cart'
    return HttpResponse(success)


# Displays all the items in the cart
def cart(request, user_id):
    user = User.objects.get(id=user_id)
    cart = Cart.objects.filter(user=user).prefetch_related('cartpizza_set__pizza')

    # retrieve the 'Offers in the cart' objects using a separate query
    cart_offer_quantities = CartOfferQuantity.objects.filter(cart__user=user)

    # group the 'Offers in the cart' objects by cart id
    cart_offer_quantities_by_cart = defaultdict(list)
    for cart_offer_quantity in cart_offer_quantities:
        cart_offer_quantities_by_cart[cart_offer_quantity.cart_id].append(cart_offer_quantity)

    # serialize the cart data to a json format to be returned in AJAX request
    data = {
        'cart': [{
            'created_at': str(item.created_at),
            'cart_sum': item.cart_sum,
            'pizza': [{
                'name': cart_pizza.pizza.name,
                'price': cart_pizza.pizza.price,
                'id': cart_pizza.pizza.id,
                'quantity': cart_pizza.quantity
            } for cart_pizza in item.cartpizza_set.all()],
            'offer': [{
                'offer_name': cart_offer_quantity.offer.offer_name,
                'offer_price': cart_offer_quantity.offer.offer_price,
                'offer_id': cart_offer_quantity.offer.id,
                'quantity': cart_offer_quantity.quantity
            } for cart_offer_quantity in cart_offer_quantities_by_cart[item.id]]
        } for item in cart
        ]}

    return JsonResponse(data)


def getPizzasInOffer(request, user_id, offer_id):
    # Start by finding the cart belonging to the user
    user = User.objects.get(id=user_id)
    # Returns all objects related to the offer containng the specific pizza
    offer_quantity = CartOfferQuantity.objects.filter(
        offer__pizza__id=offer_id,
        cart__user=user
    )
    # get all the related pizzas for the offer
    offer_quantity = offer_quantity.prefetch_related('offer__pizza')

    pizzas = []
    for single_offer in offer_quantity:
        for pizza in single_offer.offer.pizza.all():
            pizzas.append({
                'name': pizza.name
            })

    return JsonResponse(pizzas, safe=False)


def deleteOfferItem(request, user_id, offer_id):
    try:
        cart = get_object_or_404(Cart, user_id=user_id)

        offer = get_object_or_404(Offer, id=offer_id)

        cart_offer = get_object_or_404(CartOfferQuantity, cart=cart, offer=offer)

        if cart_offer.quantity > 1:
            cart_offer.quantity -= 1
            cart_offer.save()

            cart.cart_sum -= offer.offer_price

            cart.save()
        else:
            cart_offer.delete()
            cart.offer_quantity.remove(offer)
            cart.cart_sum -= offer.offer_price
            cart.save()

        return JsonResponse({'message': 'Cart item deleted successfully'})
    except Exception as e:
        print(e)
        # indicating server error
        return JsonResponse({'message': 'Error deleting item'}, status=500)


def deleteCartItem(request, user_id, pizza_id):
    try:
        # Get the Cart for this user, or throw not found
        cart = get_object_or_404(Cart, user_id=user_id)
        # Get the specific pizza, or throw not found
        pizza = get_object_or_404(Pizza, id=pizza_id)
        # get the CartPizza object for this cart and pizza
        cart_pizza = get_object_or_404(CartPizza, cart=cart, pizza=pizza)
        # if the quantity is greater than 1, decrement the quantity and save
        if cart_pizza.quantity > 1:
            cart_pizza.quantity -= 1
            cart_pizza.save()
            # re-calculate the sum
            cart.cart_sum -= pizza.price
            # update changes
            cart.save()
        else:
            # remove the CartPizza object from the cart
            cart_pizza.delete()
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
    # Get the Many to Many relation model which contains each cart item, for a specific cart
    cartpizza = CartPizza.objects.filter(cart=cart.id)
    cartoffer = CartOfferQuantity.objects.filter(cart=cart.id)
    # Returns a query seat for each pizza and offer for the specific cart
    countedPizzas = cartpizza.annotate(Count('pizza'))
    countedOffers = cartoffer.annotate(Count('offer'))
    # counts the pizzas and offers in the cart, but doesn't count the quantity property
    item_counter = cart.pizza.count() + cart.offer_quantity.count()
    # Iterate the query set, and add the quantity for the pizzas to the counter
    for item in countedPizzas:
        if item.quantity > 1:
            # Subtract 1 here, because the quantity may be 2 for example, but we've already counted that pizza once
            item_counter += item.quantity - 1
    for offer in countedOffers:
        if offer.quantity > 1:
            # Same principle as above
            item_counter += offer.quantity - 1

    # return a json response so we can display it in the DOM
    return JsonResponse({'countedItems': item_counter}, status=200)
