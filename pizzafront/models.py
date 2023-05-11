from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    CustomUserManager is a custom manager for the User model.
    It inherits from BaseUserManager and provides methods to create a user
    and create a superuser.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Added blank=True to test user registration
    Makes every field optional except email,password
    Can remove when functionality for other fields are integrated
    '''

    # name
    name = models.CharField(max_length=254, blank=True, null=True)
    # email
    email = models.EmailField(max_length=254, unique=True)
    # phoneNumber
    phone_number = models.CharField(max_length=254, blank=True, null=True)
    # streetName
    street_name = models.CharField(max_length=254, blank=True, null=True)
    # houseNumber
    house_number = models.CharField(max_length=254, blank=True, null=True)
    # city
    city = models.CharField(max_length=254, blank=True, null=True)
    # postalCode
    postal_code = models.CharField(max_length=254, blank=True, null=True)
    # password
    password = models.CharField(max_length=128)
    # img
    img = models.ImageField(upload_to='avatars/', default='default_avatar.png')

    # Required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Offer(models.Model):
    # offerName
    offer_name = models.CharField(max_length=254)
    # offerPrice
    offer_price = models.DecimalField(max_digits=254, decimal_places=2)
    # offerImage
    offer_image = models.ImageField(null=True)


class OfferPizza(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    pizza = models.ForeignKey('Pizza', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class PizzaType(models.Model):
    SPICY_CHOICE = 'S'
    VEGAN_CHOICE = 'V'

    TOPPING_CHOICE = [
        (SPICY_CHOICE, 'Spicy'),
        (VEGAN_CHOICE, 'Vegan')
    ]
    # name
    name = models.CharField(max_length=1, choices=TOPPING_CHOICE)


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

    pizza_image = models.ImageField()

    topping = models.ManyToManyField(Topping)

    pizza_type = models.ForeignKey(PizzaType, on_delete=models.RESTRICT, null=True)


class Cart(models.Model):
    # cartSum
    cart_sum = models.DecimalField(max_digits=254, decimal_places=2)
    # createdAt
    created_at = models.DateTimeField(auto_now_add=True)
    # pizzaID
    pizza = models.ManyToManyField(Pizza, through='CartPizza')
    # offerID, this is called quantity due to changes in the through M2M class, had to update the quantity.
    offer_quantity = models.ManyToManyField(
        Offer,
        through='CartOfferQuantity',
        related_name='carts_with_offer_quantity'
    )
    # userID Fk
    user = models.ForeignKey(User, on_delete=models.RESTRICT)


# New through field for the Cart To Offer relation
class CartOfferQuantity(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='offer_quantities'
    )
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


# To be able to store unique offers in the cart
class CartOffer(models.Model):
    cart_offer_quantity = models.OneToOneField(CartOfferQuantity, on_delete=models.CASCADE, related_name='cart_offer')
    pizzas = models.ManyToManyField(Pizza)


class CartPizza(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class MainMenu(models.Model):
    # offerID FK
    offer = models.ManyToManyField(Offer)


class Menu(models.Model):
    # pizzaID Fk
    pizza = models.ManyToManyField(Pizza)
