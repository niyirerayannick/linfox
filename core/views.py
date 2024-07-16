import csv
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser,Driver, Car, Destination,Deduction, FuelConsumption, ProductDelivery, Owner, CarOwnership, Payment
from django.views.generic import ListView, DetailView, View



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']
        telephone = request.POST['telephone']
        password = request.POST['password']
        password2 = request.POST['password2']
        profile_image = request.FILES.get('profile_image')

        if password != password2:
            return render(request, 'core/register.html', {'error': 'Passwords do not match'})

        user = CustomUser.objects.create(
            username=username,
            email=email,
            full_name=full_name,
            telephone=telephone,
            profile_image=profile_image,
            password=make_password(password)
        )
        login(request, user)
        return redirect('login')

    return render(request, 'core/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            form_errors = "Invalid username or password. Please try again."
            return render(request, 'core/login.html', {'form_errors': form_errors})

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home(request):
    fuel_consumptions = FuelConsumption.objects.all()
    total_drivers = Driver.objects.count()
    total_Fuel= FuelConsumption.objects.count()
    total_payment = Payment.objects.count()
    total_cars= Car.objects.count()
    return render(request, 'core/dashboard.html', {'fuel_consumptions': fuel_consumptions,
                                                   'total_drivers': total_drivers, 
                                                     'total_Fuel':total_Fuel,'total_cars':total_cars,
                                                     'total_payment':total_payment})

# Driver Views
class DriverListView(ListView):
    model = Driver
    template_name = 'drivers/driver_list.html'
    context_object_name = 'drivers'

class DriverDetailView(DetailView):
    model = Driver
    template_name = 'drivers/driver_detail.html'
    context_object_name = 'driver'

class DriverCreateView(View):
    def get(self, request):
        return render(request, 'drivers/driver_form.html')

    def post(self, request):
        name = request.POST.get('name')
        license_number = request.POST.get('license_number')
        contact_details = request.POST.get('contact_details')
        Driver.objects.create(name=name, license_number=license_number, contact_details=contact_details)
        return redirect('driver_list')

class DriverUpdateView(View):
    def get(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        return render(request, 'drivers/driver_form.html', {'driver': driver})

    def post(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        driver.name = request.POST.get('name')
        driver.license_number = request.POST.get('license_number')
        driver.contact_details = request.POST.get('contact_details')
        driver.save()
        return redirect('driver_list')

class DriverDeleteView(View):
    def get(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        return render(request, 'drivers/driver_confirm_delete.html', {'driver': driver})

    def post(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        driver.delete()
        return redirect('driver_list')

# Car Views
class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

class CarCreateView(View):
    def get(self, request):
        return render(request, 'cars/car_form.html')

    def post(self, request):
        registration_number = request.POST.get('registration_number')
        make = request.POST.get('make')
        model = request.POST.get('model')
        fuel_type = request.POST.get('fuel_type')
        Car.objects.create(registration_number=registration_number, make=make, model=model, fuel_type=fuel_type)
        return redirect('car_list')

class CarUpdateView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        return render(request, 'cars/car_form.html', {'car': car})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.registration_number = request.POST.get('registration_number')
        car.make = request.POST.get('make')
        car.model = request.POST.get('model')
        car.fuel_type = request.POST.get('fuel_type')
        car.save()
        return redirect('car_list')

class CarDeleteView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        return render(request, 'cars/car_confirm_delete.html', {'car': car})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return redirect('car_list')

# Destination Views
class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'

class DestinationCreateView(View):
    def get(self, request):
        return render(request, 'destinations/destination_form.html')

    def post(self, request):
        starting_point = request.POST.get('starting_point')
        destination_point = request.POST.get('destination_point')
        Destination.objects.create(starting_point=starting_point, destination_point=destination_point)
        return redirect('destination_list')

class DestinationUpdateView(View):
    def get(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        return render(request, 'destinations/destination_form.html', {'destination': destination})

    def post(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        destination.starting_point = request.POST.get('starting_point')
        destination.destination_point = request.POST.get('destination_point')
        destination.save()
        return redirect('destination_list')

class DestinationDeleteView(View):
    def get(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        return render(request, 'destinations/destination_confirm_delete.html', {'destination': destination})

    def post(self, request, pk):
        destination = get_object_or_404(Destination, pk=pk)
        destination.delete()
        return redirect('destination_list')

# Fuel Consumption Views
class FuelConsumptionListView(ListView):
    model = FuelConsumption
    template_name = 'fuel_consumptions/fuel_consumption_list.html'
    context_object_name = 'fuel_consumptions'

class FuelConsumptionDetailView(DetailView):
    model = FuelConsumption
    template_name = 'fuel_consumptions/fuel_consumption_detail.html'
    context_object_name = 'fuel_consumption'

class FuelConsumptionCreateView(View):
    def get(self, request):
        owners = Owner.objects.all()
        cars = Car.objects.all()
        drivers = Driver.objects.all()
        destinations = Destination.objects.all()
        context = {
            'owners': owners,
            'cars': cars,
            'drivers': drivers,
            'destinations':destinations,
        }
        return render(request, 'fuel_consumptions/fuel_consumption_form.html',context)

    def post(self, request):
        driver_id = request.POST.get('driver')
        car_id = request.POST.get('car')
        destination_id = request.POST.get('destination')
        amount_used = request.POST.get('amount_used')
        invoice_image = request.FILES.get('invoice_image')
        
        driver = get_object_or_404(Driver, id=driver_id)
        car = get_object_or_404(Car, id=car_id)
        destination = get_object_or_404(Destination, id=destination_id)
        
        FuelConsumption.objects.create(driver=driver, car=car, destination=destination, amount_used=amount_used, invoice_image=invoice_image)
        return redirect('fuel_consumption_list')

class FuelConsumptionUpdateView(View):
    def get(self, request, pk):
        owners = Owner.objects.all()
        cars = Car.objects.all()
        drivers = Driver.objects.all()
        destinations = Destination.objects.all()
        fuel_consumption = get_object_or_404(FuelConsumption, pk=pk)
        context = {
            'owners': owners,
            'cars': cars,
            'drivers': drivers,
            'destinations':destinations,
            'fuel_consumption': fuel_consumption,
        }
        
        return render(request, 'fuel_consumptions/fuel_consumption_form.html',context)

    def post(self, request, pk):
        fuel_consumption = get_object_or_404(FuelConsumption, pk=pk)
        fuel_consumption.driver = get_object_or_404(Driver, id=request.POST.get('driver'))
        fuel_consumption.car = get_object_or_404(Car, id=request.POST.get('car'))
        fuel_consumption.destination = get_object_or_404(Destination, id=request.POST.get('destination'))
        fuel_consumption.amount_used = request.POST.get('amount_used')
        if 'invoice_image' in request.FILES:
            fuel_consumption.invoice_image = request.FILES.get('invoice_image')
        fuel_consumption.save()
        return redirect('fuel_consumption_list')

class FuelConsumptionDeleteView(View):
    def get(self, request, pk):
        fuel_consumption = get_object_or_404(FuelConsumption, pk=pk)
        return render(request, 'fuel_consumptions/fuel_consumption_confirm_delete.html', {'fuel_consumption': fuel_consumption})

    def post(self, request, pk):
        fuel_consumption = get_object_or_404(FuelConsumption, pk=pk)
        fuel_consumption.delete()
        return redirect('fuel_consumption_list')

# Product Delivery Views
class ProductDeliveryListView(ListView):
    model = ProductDelivery
    template_name = 'product_deliveries/product_delivery_list.html'
    context_object_name = 'product_deliveries'

class ProductDeliveryDetailView(DetailView):
    model = ProductDelivery
    template_name = 'product_deliveries/product_delivery_detail.html'
    context_object_name = 'product_delivery'

class ProductDeliveryCreateView(View):
    def get(self, request):
        owners = Owner.objects.all()
        cars = Car.objects.all()
        drivers = Driver.objects.all()
        destinations = Destination.objects.all()
        context = {
            'owners': owners,
            'cars': cars,
            'drivers': drivers,
            'destinations':destinations,
        }

        return render(request, 'product_deliveries/product_delivery_form.html',context)

    def post(self, request):
        driver_id = request.POST.get('driver')
        car_id = request.POST.get('car')
        destination_id = request.POST.get('destination')
        product_name = request.POST.get('product_name')
        quantity_sent = request.POST.get('quantity_sent')
        quantity_received = request.POST.get('quantity_received')

        driver = get_object_or_404(Driver, id=driver_id)
        car = get_object_or_404(Car, id=car_id)
        destination = get_object_or_404(Destination, id=destination_id)

        ProductDelivery.objects.create(driver=driver, car=car, destination=destination, product_name=product_name, quantity_sent=quantity_sent, quantity_received=quantity_received)
        return redirect('product_delivery_list')

class ProductDeliveryUpdateView(View):
    def get(self, request, pk):
        product_delivery = get_object_or_404(ProductDelivery, pk=pk)
        owners = Owner.objects.all()
        cars = Car.objects.all()
        drivers = Driver.objects.all()
        destinations = Destination.objects.all()
        context = {
            'owners': owners,
            'cars': cars,
            'drivers': drivers,
            'destinations':destinations,
            'product_delivery': product_delivery
        }
        return render(request, 'product_deliveries/product_delivery_form.html',context)

    def post(self, request, pk):
        product_delivery = get_object_or_404(ProductDelivery, pk=pk)
        product_delivery.driver = get_object_or_404(Driver, id=request.POST.get('driver'))
        product_delivery.car = get_object_or_404(Car, id=request.POST.get('car'))
        product_delivery.destination = get_object_or_404(Destination, id=request.POST.get('destination'))
        product_delivery.product_name = request.POST.get('product_name')
        product_delivery.quantity_sent = request.POST.get('quantity_sent')
        product_delivery.quantity_received = request.POST.get('quantity_received')
        product_delivery.save()
        return redirect('product_delivery_list')

class ProductDeliveryDeleteView(View):
    def get(self, request, pk):
        product_delivery = get_object_or_404(ProductDelivery, pk=pk)
        return render(request, 'product_deliveries/product_delivery_confirm_delete.html', {'product_delivery': product_delivery})

    def post(self, request, pk):
        product_delivery = get_object_or_404(ProductDelivery, pk=pk)
        product_delivery.delete()
        return redirect('product_delivery_list')


def export_product_deliveries(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_deliveries.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Product Name', 'Car', 'Driver', 'Destination', 'Quantity Sent', 'Quantity Received'])

    product_deliveries = ProductDelivery.objects.all()
    for delivery in product_deliveries:
        writer.writerow([
            delivery.id,
            delivery.product_name,
            delivery.car,
            delivery.driver,
            delivery.destination,
            delivery.quantity_sent,
            delivery.quantity_received,
        ])

    return response

# Owner Views
class OwnerListView(ListView):
    model = Owner
    template_name = 'owners/owner_list.html'
    context_object_name = 'owners'

class OwnerDetailView(DetailView):
    model = Owner
    template_name = 'owners/owner_detail.html'
    context_object_name = 'owner'

class OwnerCreateView(View):
    def get(self, request):
        return render(request, 'owners/owner_form.html')

    def post(self, request):
        name = request.POST.get('name')
        contact_details = request.POST.get('contact_details')
        Owner.objects.create(name=name, contact_details=contact_details)
        return redirect('owner_list')

class OwnerUpdateView(View):
    def get(self, request, pk):
        owner = get_object_or_404(Owner, pk=pk)
        return render(request, 'owners/owner_form.html', {'owner': owner})

    def post(self, request, pk):
        owner = get_object_or_404(Owner, pk=pk)
        owner.name = request.POST.get('name')
        owner.contact_details = request.POST.get('contact_details')
        owner.save()
        return redirect('owner_list')

class OwnerDeleteView(View):
    def get(self, request, pk):
        owner = get_object_or_404(Owner, pk=pk)
        return render(request, 'owners/owner_confirm_delete.html', {'owner': owner})

    def post(self, request, pk):
        owner = get_object_or_404(Owner, pk=pk)
        owner.delete()
        return redirect('owner_list')

# Car Ownership Views
class CarOwnershipListView(ListView):
    model = CarOwnership
    template_name = 'car_ownerships/car_ownership_list.html'
    context_object_name = 'car_ownerships'

class CarOwnershipDetailView(DetailView):
    model = CarOwnership
    template_name = 'car_ownerships/car_ownership_detail.html'
    context_object_name = 'car_ownership'

class CarOwnershipCreateView(View):
    def get(self, request):
        owners = Owner.objects.all()
        cars = Car.objects.all()
        drivers = Driver.objects.all()
        context = {
            'owners': owners,
            'cars': cars,
            'drivers': drivers,
        }
        return render(request, 'car_ownerships/car_ownership_form.html',context)

    def post(self, request):
        owner_id = request.POST.get('owner')
        car_id = request.POST.get('car')
        driver_id = request.POST.get('driver')
        owner = get_object_or_404(Owner, id=owner_id)
        car = get_object_or_404(Car, id=car_id)
        driver = get_object_or_404(Driver, id=driver_id)

        CarOwnership.objects.create(owner=owner, car=car, driver=driver)
        return redirect('car_ownership_list')

class CarOwnershipUpdateView(View):
    def get(self, request, pk):
        owners = Owner.objects.all()
        cars = Car.objects.all()
        drivers = Driver.objects.all()
        car_ownership = get_object_or_404(CarOwnership, pk=pk)
        return render(request, 'car_ownerships/car_ownership_form.html', {'car_ownership': car_ownership, 'owners': owners, 'drivers': drivers, 'cars': cars})

    def post(self, request, pk):
        car_ownership = get_object_or_404(CarOwnership, pk=pk)
        car_ownership.owner = get_object_or_404(Owner, id=request.POST.get('owner'))
        car_ownership.car = get_object_or_404(Car, id=request.POST.get('car'))
        car_ownership.driver = get_object_or_404(Driver, id=request.POST.get('driver'))
        car_ownership.save()
        return redirect('car_ownership_list')

class CarOwnershipDeleteView(View):
    def get(self, request, pk):
        car_ownership = get_object_or_404(CarOwnership, pk=pk)
        return render(request, 'car_ownerships/car_ownership_confirm_delete.html', {'car_ownership': car_ownership})

    def post(self, request, pk):
        car_ownership = get_object_or_404(CarOwnership, pk=pk)
        car_ownership.delete()
        return redirect('car_ownership_list')



class DeductionListView(ListView):
    model = Deduction
    template_name = 'deductions/deductions_list.html'
    context_object_name = 'deductions'


# Payment Views
class PaymentListView(ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'

class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'
from django.contrib import messages
class PaymentFormView(View):
    def get(self, request, pk=None):
        if pk:
            payment = get_object_or_404(Payment, pk=pk)
            car_ownerships = CarOwnership.objects.all()
            context = {
                'payment': payment,
                'car_ownerships': car_ownerships,
                'is_update': True
            }
        else:
            car_ownerships = CarOwnership.objects.all()
            context = {
                'car_ownerships': car_ownerships,
                'is_update': False
            }
        return render(request, 'payments/payment_form.html', context)

    def post(self, request, pk=None):
        car_ownership_id = request.POST.get('car_ownership')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        invoice_details = request.POST.get('invoice_details')

        if not all([car_ownership_id, amount, payment_date, payment_method, invoice_details]):
            messages.error(request, 'All fields are required.')
            if pk:
                return redirect('payment_update', pk=pk)
            else:
                return redirect('payment_create')

        car_ownership = get_object_or_404(CarOwnership, id=car_ownership_id)

        if pk:
            payment = get_object_or_404(Payment, pk=pk)
            payment.car_ownership = car_ownership
            payment.amount = amount
            payment.payment_date = payment_date
            payment.payment_method = payment_method
            payment.invoice_details = invoice_details
            payment.save()
            messages.success(request, 'Payment updated successfully.')
        else:
            Payment.objects.create(
                car_ownership=car_ownership,
                amount=amount,
                payment_date=payment_date,
                payment_method=payment_method,
                invoice_details=invoice_details
            )
            messages.success(request, 'Payment created successfully.')

        return redirect('payment_list')

class PaymentDeleteView(View):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'payments/payment_confirm_delete.html', {'payment': payment})

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return redirect('payment_list')



# @receiver(post_save, sender=FuelConsumption)
# def create_invoice_for_fuel_consumption(sender, instance, created, **kwargs):
#     if created:
#         invoice_number = f"FC-{instance.id:06d}"
#         Invoice.objects.create(invoice_number=invoice_number, fuel_consumption=instance, payment=instance.payment_set.first())

# @receiver(post_save, sender=Payment)
# def create_invoice_for_payment(sender, instance, created, **kwargs):
#     if created:
#         invoice_number = f"PAY-{instance.id:06d}"
#         Invoice.objects.create(invoice_number=invoice_number, payment=instance, fuel_consumption=instance.car_ownership.car.fuelconsumption_set.first())
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from .models import Invoice

# def generate_invoice_pdf(request, invoice_id):
#     invoice = Invoice.objects.get(id=invoice_id)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

#     doc = SimpleDocTemplate(response, pagesize=letter)
#     elements = []

#     styles = getSampleStyleSheet()
#     header = Paragraph(f"Invoice Number: {invoice.invoice_number}", styles['Title'])
#     date_issued = Paragraph(f"Date Issued: {invoice.date_issued}", styles['Normal'])
#     elements.extend([header, date_issued])

#     # Fuel Consumption Details
#     fuel_data = [
#         ['Driver', invoice.fuel_consumption.driver.name],
#         ['Car', invoice.fuel_consumption.car.registration_number],
#         ['Destination', f"{invoice.fuel_consumption.destination}"],
#         ['Amount Used', f"{invoice.fuel_consumption.amount_used}L"],
#         ['Total Cost', f"{invoice.fuel_consumption.amount_used} USD"]
#     ]

#     fuel_table = Table(fuel_data)
#     fuel_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(fuel_table)

#     # Payment Details
#     payment_data = [
#         ['Amount', f"{invoice.payment.amount} USD"],
#         ['Payment Date', invoice.payment.payment_date],
#         ['Payment Method', invoice.payment.payment_method],
#         ['Invoice Details', invoice.payment.invoice_details]
#     ]

#     payment_table = Table(payment_data)
#     payment_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(payment_table)

#     doc.build(elements)
#     return response
