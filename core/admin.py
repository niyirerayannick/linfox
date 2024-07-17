from django.contrib import admin
from .models import (CustomUser, Driver, Owner, Car, Destination,
                     FuelConsumption, ProductDelivery, CarOwnership,
                     Payment, Deduction, Invoice)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'telephone']
    search_fields = ['username', 'full_name']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_number']
    search_fields = ['name', 'license_number']

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'Owner_ids']
    search_fields = ['name']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'chassis_number', 'model', 'fuel_type', 'owner', 'driver']
    search_fields = ['registration_number', 'model']
    list_filter = ['owner', 'driver']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['starting_point', 'destination_point']
    search_fields = ['starting_point', 'destination_point']

@admin.register(FuelConsumption)
class FuelConsumptionAdmin(admin.ModelAdmin):
    list_display = ['car', 'owner', 'driver', 'destination', 'amount_used']
    search_fields = ['car__registration_number', 'driver__name', 'destination__starting_point']
    list_filter = ['driver', 'car', 'destination']

@admin.register(ProductDelivery)
class ProductDeliveryAdmin(admin.ModelAdmin):
    list_display = ['driver', 'car', 'destination', 'product_category', 'quantity_sent', 'quantity_received']
    search_fields = ['driver__name', 'car__registration_number', 'destination__starting_point']
    list_filter = ['driver', 'car', 'destination']

@admin.register(CarOwnership)
class CarOwnershipAdmin(admin.ModelAdmin):
    list_display = ['owner', 'car', 'driver']
    search_fields = ['owner__name', 'car__registration_number', 'driver__name']
    list_filter = ['owner', 'car', 'driver']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['car_ownership', 'amount_per_day', 'total_amount', 'payment_date', 'payment_method']
    search_fields = ['car_ownership__owner__name', 'car_ownership__car__registration_number']
    list_filter = ['payment_date', 'payment_method']

@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ['car_ownership', 'car', 'deduction_date', 'fuel_advance', 'cash_advance']
    search_fields = ['car_ownership__owner__name', 'car__registration_number']
    list_filter = ['deduction_date']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'date_issued', 'amount_due', 'payment_status', 'remaining_balance']
    search_fields = ['invoice_number', 'owner__name']
    list_filter = ['payment_status']
