from django.shortcuts import render
from django.views import View 
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AdminRegistrationForm, CustomerRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")

@login_required
def customer_dashboard(request):
    return render(request, "dashboard/customer_dashboard.html")


class IndexView(TemplateView):
    template_name = "index.html"


class AdminRegistrationView(View):
    template_name = "admin_register.html"

    def get(self, request, *args, **kwargs):
        form = AdminRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AdminRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin registered successfully.")
            return redirect("login")  # Redirect to login after successful registration
        messages.error(request, "Error in form submission. Please check the details.")
        return render(request, self.template_name, {"form": form})


class CustomerRegistrationView(View):
    template_name = "customer_register.html"

    def get(self, request, *args, **kwargs):
        form = CustomerRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer registered successfully.")
            return redirect("login")  # Redirect to login after successful registration
        messages.error(request, "Error in form submission. Please check the details.")
        return render(request, self.template_name, {"form": form})



class LoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        # If the user is already logged in, check the role and redirect accordingly
        if request.user.is_authenticated:
            return self.redirect_user_based_on_role(request.user)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get username and password from POST request
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return self.redirect_user_based_on_role(user)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name)

    def redirect_user_based_on_role(self, user):
        # Check the user's role and redirect to the appropriate dashboard
        if user.role == "admin":
            return redirect("admin_dashboard")  # Replace with your admin dashboard URL
        elif user.role == "customer":
            return redirect("customer_dashboard")  # Replace with your customer dashboard URL
        else:
            return redirect("login")  # Fallback: redirect to login if no matching role
