from django.urls import path
from .views import*

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path('register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('login/', LoginView.as_view(), name='login'),
]
