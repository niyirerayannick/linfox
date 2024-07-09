from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser,Driver, Car, Destination, FuelConsumption, ProductDelivery, Owner, CarOwnership, Payment
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
    return render(request, 'core/dashboard.html')

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
        return render(request, 'fuel_consumptions/fuel_consumption_form.html')

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
        fuel_consumption = get_object_or_404(FuelConsumption, pk=pk)
        return render(request, 'fuel_consumptions/fuel_consumption_form.html', {'fuel_consumption': fuel_consumption})

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
        return render(request, 'product_deliveries/product_delivery_form.html')

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
        return render(request, 'product_deliveries/product_delivery_form.html', {'product_delivery': product_delivery})

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
        return render(request, 'car_ownerships/car_ownership_form.html')

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
        car_ownership = get_object_or_404(CarOwnership, pk=pk)
        return render(request, 'car_ownerships/car_ownership_form.html', {'car_ownership': car_ownership})

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

# Payment Views
class PaymentListView(ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'

class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'

class PaymentCreateView(View):
    def get(self, request):
        return render(request, 'payments/payment_form.html')

    def post(self, request):
        owner_id = request.POST.get('owner')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        owner = get_object_or_404(Owner, id=owner_id)
        Payment.objects.create(owner=owner, amount=amount, date=date)
        return redirect('payment_list')

class PaymentUpdateView(View):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'payments/payment_form.html', {'payment': payment})

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.owner = get_object_or_404(Owner, id=request.POST.get('owner'))
        payment.amount = request.POST.get('amount')
        payment.date = request.POST.get('date')
        payment.save()
        return redirect('payment_list')

class PaymentDeleteView(View):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'payments/payment_confirm_delete.html', {'payment': payment})

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return redirect('payment_list')
