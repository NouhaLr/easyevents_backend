# rfid/urls.py
from django.urls import path
from .views import assign_bracelet, simulate_scan_purchase

urlpatterns = [
    path('assign/', assign_bracelet, name='assign_bracelet'),
    path('simulate-scan/', simulate_scan_purchase, name='simulate_scan_purchase'),
]
