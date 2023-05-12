import json
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pizzafront.models import *
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Prefetch, Subquery, Q
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from django.urls import reverse

from .forms import RegisterForm


# Create your views here.

# Error handling views, for 500 and 404.
def handler404(request, exception):
    return render(request, '404.html', status=400)


def handler500(request):
    return render(request, '500.html', status=500)


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


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST['name']
        user.street_name = request.POST['street_name']
        user.house_number = request.POST['house_number']
        user.city = request.POST['city']
        user.country = request.POST['country']
        user.postal_code = request.POST['postal_code']
        if 'img' in request.FILES:
            user.img = request.FILES['img']
        user.save()
        messages.success(request, 'Profile information updated successfully.')

        return redirect('menu')

    return render(request, 'profile.html')


def addPizzaToOffer(request, offer_id):
    # Start by getting the user that's logged in
    user = request.user
    # find the selected offer
    offer = Offer.objects.get(id=offer_id)

    # get the cart
    cart = Cart.objects.get(user=user)

    # pizza_id_list:
    # this is sent as the post req. body
    data = json.loads(request.body)
    pizza_id_list = data.get('pizza_id_list', [])
    # iterate the pizza ids in the list
    for pizzaID in pizza_id_list:
        OfferPizza.objects.create(offer=offer, pizza_id=pizzaID)

    # save changes
    offer.save()

    #######
    # CartOfferQuantity holds how many dubplicate offers we have, so if I select the same one twice, we upp the quant.
    ########

    # check if a CartOfferQuantity object already exists for this cart and offer
    # This is so we can have dublicate offers
    cart_offer_item = CartOfferQuantity.objects.filter(cart=cart, offer=offer).first()
    if cart_offer_item:
        # If the CartOfferQuantity object already exists, increment its quantity by 1
        cart_offer_item.quantity += 1
        cart_offer_item.save()
    else:
        # Create a new CartOfferQuantity object with a quantity of 1
        cart_offer_item = CartOfferQuantity.objects.create(cart=cart, offer=offer, quantity=1)

    # increment the price
    cart.cart_sum += offer.offer_price

    # add the cart offer to the cart
    return addOfferToCart(request, cart, offer)


# Decided to split it up at least a bit, so this is a 'helper function' to finalize the cart addition
def addOfferToCart(request, cart, offer):
    # Add the offer to the cart
    cart.offer_quantity.add(offer)
    # Update the cart total sum
    cart.save()

    return HttpResponse('Successfully added offer to cart!', status=201)


@login_required
def addToCart(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)

    user = request.user

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
    return HttpResponse(success, status=201)


# Displays all the items in the cart
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user).prefetch_related('cartpizza_set__pizza')

    # retrieve the 'Offers in the cart' objects using a separate query
    cart_offer_quantities = CartOfferQuantity.objects.filter(cart__user=user)

    # group the 'Offers in the cart' objects by cart id
    cart_offer_quantities_by_cart = defaultdict(list)
    for cart_offer_quantity in cart_offer_quantities:
        cart_offer_quantities_by_cart[cart_offer_quantity.cart_id].append(cart_offer_quantity)

    # serialize the cart data to a json format to be returned in AJAX request
    # using list comprehension to populate:
    # A. a pizza list, containing the Attributes we want from the Pizza Model
    # B. an offer list, also containing Attributes we want but, from the Offer Model.
    # -- These items are then stored in a cart list, which we use to access on the front-end
    # Additionally this format is used (list containing dict) to be used as an object in javascript
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

    return JsonResponse(data, status=200)


def getPizzasInOffer(request, offer_id):
    # select the offer, based on given offer_id from frontend
    offer = Offer.objects.get(id=offer_id)
    # get all the pizzas in the offer
    pizzas = offer.offerpizza_set.all().values('pizza__name')
    # create a list out of the query-set
    pizza_list = list(pizzas)
    # Make a dict that can be returned as an object to the Javascript with the pizza_list
    response_data = {'pizzas': pizza_list}
    return JsonResponse(response_data, safe=False, status=200)


def deleteOfferItem(request, offer_id):
    # Safe fails in place, incase we cannot retrieve, cart, offer or CartOfferPizza
    # the get_object_or_404, as the name indicates 404's if we can't find the relevent information
    # hence the try / except
    try:
        # Start by trying to get the user's cart
        cart = get_object_or_404(Cart, user_id=request.user)
        # then offer
        offer = get_object_or_404(Offer, id=offer_id)
        # Then the CartOfferQuantity, m2m relation with Cart, holds quantity of dublicate offers
        cart_offer = get_object_or_404(CartOfferQuantity, cart=cart, offer=offer)
        # Get all the pizzas in the offer, OfferPizza is an M2M with Offers and Pizzas
        offer_pizzas = OfferPizza.objects.filter(offer=offer)
        # Iterate the pizzas in the offer and delete all of them
        for offer_pizza in offer_pizzas:
            offer_pizza.delete()
        # in order to reduce the price for dublicate offers, we need to check
        # if the quantity is greater then 1,
        # iterate n*quantity and reduce the cart sum.
        if cart_offer.quantity > 1:
            for _ in range(0, cart_offer.quantity):
                cart.cart_sum -= offer.offer_price
        else:
            cart.cart_sum -= offer.offer_price

        # Delete the offer and remove it from the CartOfferQuantity model
        # Save changes
        cart_offer.delete()

        cart.offer_quantity.remove(offer)

        cart.save()

        return JsonResponse({'message': 'Cart item deleted successfully'})
    except Exception as e:
        print(e)
        # indicating server error, incase we don't find or cannot delete certain items
        return HttpResponseServerError()


# User cannot access this unless he is logged in.
def deleteWholeCart(request):
    # Get the cart for the logged in user
    cart = Cart.objects.get(user_id=request.user)
    # Get all the pizzas in the Cart and delete them
    CartPizza.objects.filter(cart=cart).delete()
    # Get all the offers in the Cart, through the M2M CartOfferQuantity
    cart_offer_quantities = CartOfferQuantity.objects.filter(cart=cart)
    # 'coq' just short for cart_offer_quantity in singular:
    for coq in cart_offer_quantities:
        offer = coq.offer
        OfferPizza.objects.filter(offer=offer).delete()
        cart.offer_quantity.remove(offer)

    cart_offer_quantities.delete()

    cart.cart_sum = 0
    cart.save()

    return HttpResponse('Yay, empty cart, happy heart!', status=200)


def deleteCartItem(request, pizza_id):
    try:
        # Get the Cart for this user, or throw not found
        cart = get_object_or_404(Cart, user_id=request.user)
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
        return JsonResponse({'message': 'Cart item deleted successfully'}, status=201)
    except Exception as e:
        print(e)
        # indicating server error
        return HttpResponseServerError()


# Return the sum of the cart
def cartSum(request):
    # Get the Cart for this user, or throw not found
    cart = get_object_or_404(Cart, user_id=request.user)

    totalAmount = cart.cart_sum

    return JsonResponse({'totalAmount': totalAmount}, status=200)


# Return the amount of items currently in the cart
def countCart(request):
    # Get the cart for this user, or throw not found
    try:
        # cart = get_object_or_404(Cart, user_id=user_id)
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_sum='0.00', user=request.user)

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


def checkout(request):
    context = {
        "user": request.user
    }
    return render(request, 'checkout.html', context)
