from django.urls import path
from .views import generate_invoice

urlpatterns = [
    path('invoice/<int:customer_id>/', generate_invoice, name='generate_invoice'),
]
