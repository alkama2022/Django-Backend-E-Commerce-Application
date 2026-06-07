from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Customer(models.Model):
    MEMBER_SHIP_BRONZE = 'B'
    MEMBER_SHIP_SILVER = 'S'
    MEMBER_SHIP_GOLD = 'G'
    MEMBER_SHIP_CHOICES = [
        (MEMBER_SHIP_BRONZE, 'Bronze'),
        (MEMBER_SHIP_SILVER, 'Silver'),
        (MEMBER_SHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    member_ship = models.CharField(max_length=1, choices=MEMBER_SHIP_CHOICES, default=MEMBER_SHIP_BRONZE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETED, 'Completed'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    