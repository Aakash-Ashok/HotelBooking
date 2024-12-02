from django.urls import path
from .views import AdminRegistrationView, CustomerRegistrationView,LoginView,admin_dashboard,customer_dashboard,IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/admin/", AdminRegistrationView.as_view(), name="admin_register"),
    path("register/customer/", CustomerRegistrationView.as_view(), name="customer_register"),
    path("login/", LoginView.as_view(), name="login"),
    # Add URLs for your dashboards
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/customer/", customer_dashboard, name="customer_dashboard"),
]
