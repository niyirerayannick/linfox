from django.urls import path
from .views import (register, home, user_login,logout_view,DriverListView, DriverDetailView, DriverCreateView, DriverUpdateView, DriverDeleteView,
    CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView,
    DestinationListView, DestinationDetailView, DestinationCreateView, DestinationUpdateView, DestinationDeleteView,
    FuelConsumptionListView, FuelConsumptionDetailView, FuelConsumptionCreateView, FuelConsumptionUpdateView, FuelConsumptionDeleteView,
    ProductDeliveryListView, ProductDeliveryDetailView, ProductDeliveryCreateView, ProductDeliveryUpdateView, ProductDeliveryDeleteView,
    OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView,
    CarOwnershipListView, CarOwnershipDetailView, CarOwnershipCreateView, CarOwnershipUpdateView, CarOwnershipDeleteView,
    PaymentListView, PaymentDetailView, PaymentCreateView, PaymentUpdateView, PaymentDeleteView
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),   
    path('drivers/', DriverListView.as_view(), name='driver_list'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver_detail'),
    path('drivers/create/', DriverCreateView.as_view(), name='driver_create'),
    path('drivers/<int:pk>/update/', DriverUpdateView.as_view(), name='driver_update'),
    path('drivers/<int:pk>/delete/', DriverDeleteView.as_view(), name='driver_delete'),
    
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    
    path('destinations/', DestinationListView.as_view(), name='destination_list'),
    path('destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination_detail'),
    path('destinations/create/', DestinationCreateView.as_view(), name='destination_create'),
    path('destinations/<int:pk>/update/', DestinationUpdateView.as_view(), name='destination_update'),
    path('destinations/<int:pk>/delete/', DestinationDeleteView.as_view(), name='destination_delete'),
    
    path('fuel-consumptions/', FuelConsumptionListView.as_view(), name='fuel_consumption_list'),
    path('fuel-consumptions/<int:pk>/', FuelConsumptionDetailView.as_view(), name='fuel_consumption_detail'),
    path('fuel-consumptions/create/', FuelConsumptionCreateView.as_view(), name='fuel_consumption_create'),
    path('fuel-consumptions/<int:pk>/update/', FuelConsumptionUpdateView.as_view(), name='fuel_consumption_update'),
    path('fuel-consumptions/<int:pk>/delete/', FuelConsumptionDeleteView.as_view(), name='fuel_consumption_delete'),
    
    path('product-deliveries/', ProductDeliveryListView.as_view(), name='product_delivery_list'),
    path('product-deliveries/<int:pk>/', ProductDeliveryDetailView.as_view(), name='product_delivery_detail'),
    path('product-deliveries/create/', ProductDeliveryCreateView.as_view(), name='product_delivery_create'),
    path('product-deliveries/<int:pk>/update/', ProductDeliveryUpdateView.as_view(), name='product_delivery_update'),
    path('product-deliveries/<int:pk>/delete/', ProductDeliveryDeleteView.as_view(), name='product_delivery_delete'),
    
    path('owners/', OwnerListView.as_view(), name='owner_list'),
    path('owners/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('owners/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/update/', OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
    
    path('car-ownerships/', CarOwnershipListView.as_view(), name='car_ownership_list'),
    path('car-ownerships/<int:pk>/', CarOwnershipDetailView.as_view(), name='car_ownership_detail'),
    path('car-ownerships/create/', CarOwnershipCreateView.as_view(), name='car_ownership_create'),
    path('car-ownerships/<int:pk>/update/', CarOwnershipUpdateView.as_view(), name='car_ownership_update'),
    path('car-ownerships/<int:pk>/delete/', CarOwnershipDeleteView.as_view(), name='car_ownership_delete'),
    
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
]



