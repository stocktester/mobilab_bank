from django.urls import path

from . import views

urlpatterns = [
    path('customer/', views.CustomerListView.as_view(), name='customer'),
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
]
