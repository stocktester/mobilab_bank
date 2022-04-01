from django.urls import path

from . import views

app_name = "bank"

urlpatterns = [
    path('customer/', views.CustomerListView.as_view(), name='customer'),
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('account/', views.AccountListView.as_view(), name='account'),
    path('account/<int:pk>', views.AccountDetailView.as_view(), name='account_detail')
]
