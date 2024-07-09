from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username


# Fuel Management

class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    contact_details = models.TextField()

    def __str__(self):
        return self.name

class Car(models.Model):
    registration_number = models.CharField(max_length=50)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"

class Destination(models.Model):
    starting_point = models.CharField(max_length=100)
    destination_point = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.starting_point} to {self.destination_point}"

class FuelConsumption(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    amount_used = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_image = models.ImageField(upload_to='invoices/')

    def __str__(self):
        return f"{self.driver.name} - {self.car.registration_number} - {self.amount_used}L"

# Destination Management (Product Delivery)

class ProductDelivery(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity_sent = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - {self.quantity_sent} sent - {self.quantity_received} received"

# Owner/Car/Driver Management

class Owner(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()

    def __str__(self):
        return self.name

class CarOwnership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.name} owns {self.car.registration_number} driven by {self.driver.name}"

# Payment

class Payment(models.Model):
    car_ownership = models.ForeignKey(CarOwnership, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    invoice_details = models.TextField()

    def __str__(self):
        return f"{self.amount} paid on {self.payment_date} by {self.car_ownership.owner.name}"
