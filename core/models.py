from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.db import models
from django.utils import timezone

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
    Owner_ids = models.DecimalField(max_digits=20, decimal_places=2)
    contact_details = models.TextField()

    def __str__(self):
        return self.name

class Car(models.Model):
    FUSO_LC = 'Fuso L.C'
    FUSO_BEN = 'Fuso Ben'
    DAIHATSU = 'Daihatsu'
    PICK_UP = 'Pick-up'
    ACTROS = 'Actros'

    MODEL_CHOICES = [
        (FUSO_LC, 'Fuso L.C'),
        (FUSO_BEN, 'Fuso Ben'),
        (DAIHATSU, 'Daihatsu'),
        (PICK_UP, 'Pick-up'),
        (ACTROS, 'Actros'),
    ]

    MAZUTU = 'mazutu'
    ESSENSE = 'essense'

    FUEL_TYPE_CHOICES = [
        (MAZUTU, 'Mazutu'),
        (ESSENSE, 'Essense'),
    ]

    registration_number = models.CharField(max_length=50)
    chassis_number = models.CharField(max_length=50)
    model = models.CharField(max_length=20, choices=MODEL_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.model} ({self.registration_number})"

class Destination(models.Model):
    starting_point = models.CharField(max_length=100)
    destination_point = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.starting_point} to {self.destination_point}"

class FuelConsumption(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    amount_used = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_image = models.ImageField(upload_to='invoices/')

    def __str__(self):
        return f"{self.owner.name} - {self.car.registration_number} - {self.amount_used}L"

# Product Delivery Management
class ProductDelivery(models.Model):
    SEED = 'seed'
    FERTILIZER = 'fertilizer'
    NON_AGRICULTURE = 'non_agriculture'
    
    PRODUCT_CATEGORY_CHOICES = [
        (SEED, 'Seed'),
        (FERTILIZER, 'Fertilizer'),
        (NON_AGRICULTURE, 'Non-Agriculture'),
    ]
    car_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    delivery_date = models.DateField(default=timezone.now) #VALIDETION TO COUNT DAYS
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    truck_number = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    product_category = models.CharField(max_length=20, choices=PRODUCT_CATEGORY_CHOICES, default=SEED) 
    quantity_sent = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)
    tms = models.FileField(upload_to='tms/')
    
    def number_of_days(self):
        # Assuming you want to count unique delivery dates
        return ProductDelivery.objects.filter(car=self.car).values_list('delivery_date', flat=True).distinct().count()

    def calculate_amount_due(self):
        # Assuming number_of_days is calculated based on unique delivery dates
        return self.price_per_day * self.number_of_days

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
    MOMO = 'momo'
    BANK_TRANSFER = 'bank_transfer'
    CHEQUE = 'cheque'
    PAYMENT_METHOD_CHOICES = [
        (MOMO, 'Mobile Money'),
        (BANK_TRANSFER, 'Bank Transfer'),
        (CHEQUE, 'Cheque'),
    ]
    
    car_ownership = models.ForeignKey(CarOwnership, on_delete=models.CASCADE)
    car_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    delivery_dates = models.ManyToManyField(ProductDelivery)  # Associate multiple delivery dates
    amount_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    extra_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.total_amount} paid on {self.payment_date} by {self.car_owner.name}"

    def save(self, *args, **kwargs):
        # Count unique delivery dates to determine the number of days
        unique_days = self.delivery_dates.values_list('delivery_date', flat=True).distinct().count()
        self.total_amount = (self.amount_per_day * unique_days) + self.extra_amount
        super().save(*args, **kwargs)


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


class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = [
        ('full_paid', 'Full Paid'),
        ('partial_paid', 'Partial Paid'),
    ]

    invoice_number = models.AutoField(primary_key=True)
    date_issued = models.DateField(auto_now_add=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=[
        ('momo', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ])
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    product_delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE)

    # Deduction fields
    fuel_advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    truck_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    variance_in_fuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Get the amount due from ProductDelivery
        self.amount_due = self.product_delivery.price_per_day * self.product_delivery.number_of_days()

        # Calculate total deductions for this invoice
        total_deductions = Deduction.objects.filter(car=self.car).aggregate(
            total_fuel_advance=Sum('fuel_advance'),
            total_cash_advance=Sum('cash_advance'),
            total_truck_balance=Sum('truck_balance'),
            total_variance_in_fuel=Sum('variance_in_fuel')
        )
        
        # Assign deductions to the invoice
        self.fuel_advance = total_deductions['total_fuel_advance'] or 0
        self.cash_advance = total_deductions['total_cash_advance'] or 0
        self.truck_balance = total_deductions['total_truck_balance'] or 0
        self.variance_in_fuel = total_deductions['total_variance_in_fuel'] or 0

        # Calculate total deductions
        total_deduction_amount = (
            self.fuel_advance + 
            self.cash_advance + 
            self.truck_balance + 
            self.variance_in_fuel
        )
        
        # Adjust amount due with total deductions
        self.amount_due -= total_deduction_amount
        
        # Calculate remaining balance
        self.remaining_balance = self.amount_due - self.amount_paid
        
        # Set payment status
        self.payment_status = 'full_paid' if self.remaining_balance <= 0 else 'partial_paid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.amount_due} due"
