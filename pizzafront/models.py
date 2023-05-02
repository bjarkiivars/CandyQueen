from django.db import models


# TODO:
# 1. User tengist Cart 0 to Many
# 2. Cart hefur FK: user, offer og pizza (allt 0 to Many)
# 3. Offer tengist Cart, hefur PizzaID FK, (1 to Manu)
# 4. Pizza hefurr ToppingID FK (2 to Many)
# 5. Topping
# 6. MainMenu hefur OfferID Fk, (3 to Many)
# 7. Menu hefur PizzaID fk

# Create your models here.
class User(models.Model):
    pass
    # userId PK
    # email
    # phoneNumber
    # streetName
    # houseNumber
    # city
    # postalCode
    # password
    # img


class Cart(models.Model):
    pass
    # cartID PK
    # cartSum
    # pizzaID FK
    # offerID Fk
    # userID Fk


class Offer(models.Model):
    pass
    # offerID PK
    # offerName
    # offerPrice
    # pizzaID FK


class Pizza(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    PIZZA_CHOICE = [
        ('S', '9"'),
        ('M', '12"'),
        ('L', '16"')
    ]

    size = models.CharField(max_length=1, choices=PIZZA_CHOICE)


class Topping(models.Model):
    pass
    # toppingID PK
    # name


class MainMenu(models.Model):
    pass
    # mainID PK
    # offerID FK


class Menu(models.Model):
    pass
    # menuID pk
    # pizzaID Fk
