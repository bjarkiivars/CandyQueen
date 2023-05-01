from django.db import models


# Create your models here.
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



