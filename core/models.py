from django.contrib.auth.models import AbstractUser
from django.db import models

# User Management
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

# Owner/Car/Driver Management
class Owner(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()

    def __str__(self):
        return self.name

class Car(models.Model):
    registration_number = models.CharField(max_length=50)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)


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

# Product Delivery Management
class ProductDelivery(models.Model):
    car_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    delivery_date = models.DateField()#VALIDETION TO COUNT DAYS
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    truck_number = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    product_category = models.CharField(max_length=100)
    quantity_sent = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)
    tms = models.FileField(upload_to='tms/')


    def __str__(self):
        return f"{self.product_category} - {self.quantity_sent} sent - {self.quantity_received} received"

# Car Ownership and Payment
class CarOwnership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.name} owns {self.car.registration_number} driven by {self.driver.name}"

class Payment(models.Model):
    car_ownership = models.ForeignKey(CarOwnership, on_delete=models.CASCADE)
    # fuel_consumption = models.ForeignKey(FuelConsumption, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    invoice_details = models.TextField()

    def __str__(self):
        return f"{self.amount} paid on {self.payment_date} by {self.car_ownership.owner.name}"


class Deduction(models.Model):
    car_ownership = models.ForeignKey(CarOwnership, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    deduction_date = models.DateField()
    fuel_advance = models.DecimalField(max_digits=10, decimal_places=2)
    cash_advance = models.DecimalField(max_digits=10, decimal_places=2)
    truck_balance = models.DecimalField(max_digits=10, decimal_places=2)
    varriance_in_fuel = models.DecimalField(max_digits=10, decimal_places=2)
    deduction_proof = models.FileField(upload_to='proof/')

    def __str__(self):
        return f"deduction to {self.car_ownership.owner.name}"
# from django.utils import timezone
# from django.urls import reverse
# class Invoice(models.Model):
#     invoice_number = models.CharField(max_length=50, unique=True)
#     date_issued = models.DateField(default=timezone.now)
#     fuel_consumption = models.ForeignKey(FuelConsumption, on_delete=models.CASCADE)
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

#     def get_absolute_url(self):
#         return reverse('invoice_pdf', args=[str(self.id)])

#     def __str__(self):
#         return self.invoice_number