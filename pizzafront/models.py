from django.db import models


# Create your models here.
class User(models.Model):
    # name
    name = models.CharField(max_length=254)
    # email
    email = models.EmailField(max_length=254)
    # phoneNumber
    phone_number = models.CharField(max_length=254)
    # streetName
    street_name = models.CharField(max_length=254, null=True)
    # houseNumber
    house_number = models.CharField(max_length=254, null=True)
    # city
    city = models.CharField(max_length=254, null=True)
    # postalCode
    postal_code = models.CharField(max_length=254, null=True)
    # password
    password = models.CharField(max_length=254)
    # img
    img = models.ImageField()


class Offer(models.Model):
    # offerName
    offer_name = models.CharField(max_length=254)
    # offerPrice
    offer_price = models.DecimalField(max_digits=254, decimal_places=2)
    # pizzaID FK
    pizza = models.ManyToManyField('Pizza')


class Topping(models.Model):
    # name
    name = models.CharField(max_length=254)


class Pizza(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    PIZZA_SMALL = 'S'
    PIZZA_MEDIUM = 'M'
    PIZZA_LARGE = 'L'

    PIZZA_CHOICE = [
        (PIZZA_SMALL, '9"'),
        (PIZZA_MEDIUM, '12"'),
        (PIZZA_LARGE, '16"')
    ]

    size = models.CharField(max_length=1, choices=PIZZA_CHOICE)

    topping = models.ManyToManyField(Topping)


class Cart(models.Model):
    # cartSum
    cart_sum = models.DecimalField(max_digits=254, decimal_places=2)
    # createdAt
    created_at = models.DateTimeField(auto_now_add=True)
    # pizzaID
    pizza = models.ManyToManyField(Pizza)
    # offerID Fk
    offer = models.ManyToManyField(Offer)
    # userID Fk
    user = models.ForeignKey(User, on_delete=models.RESTRICT)


class MainMenu(models.Model):
    # offerID FK
    offer = models.ManyToManyField(Offer)


class Menu(models.Model):
    # pizzaID Fk
    pizza = models.ManyToManyField(Pizza)
