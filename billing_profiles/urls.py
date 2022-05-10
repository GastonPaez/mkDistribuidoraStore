from django.urls import path
from . import views

app_name = 'billing_profiles'

urlpatterns = [

    path('', views.BillingProfileListView.as_view(), name='billing_profile'),
    path('nuevo', views.create, name='create'),
]
