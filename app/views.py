# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import *
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404


class IndexView(TemplateView):
    template_name="index.html"
    
    
class CustomerRegisterView(View):
    def get(self, request):
        return render(request, 'login.html')  # Return the sign-up page

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('customer_register')  # Stay on the signup page

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after successful registration
        except:
            messages.error(request, 'Username already exists')
            return redirect('customer_register')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            # Redirect based on user role
            if user.role == 'admin':
                return redirect('adminindex')  # Redirect to custom admin dashboard
            else:
                return redirect('customer_dashboard')  # Redirect to customer dashboard
            messages.success(request, 'You have been logged in successfully.')
        else:
            messages.error(request, 'Invalid username or password.')
        
        return render(request, self.template_name)  # Re-render the login form with error message

class LogoutView(View):
    def get(self, request):
        logout(request)  # Log out the user
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')


class AdminIndexView(TemplateView):
    template_name="admin/base_generic.html"

# List View for Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'admin/category_list.html'
    context_object_name = 'categories'

# Create View for Category
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/category_form.html'
    success_url = reverse_lazy('category_list')

# Update View for Category
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/category_form.html'
    success_url = reverse_lazy('category_list')

# Delete View for Category
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'admin/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    

# Create View for Seasonal Pricing
class SeasonalPricingCreateView(CreateView):
    model = SeasonalPricing
    form_class = SeasonalPricingForm
    template_name = 'admin/seasonalpricing_add.html'
    
    def get_initial(self):
        initial = super().get_initial()
        # Pass the category from the URL into the form's initial data
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        initial['category'] = category
        return initial

    def form_valid(self, form):
        form.instance.category = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return super().form_valid(form)

    success_url = reverse_lazy('seasonalpricing_list')
# Seasonal Pricing List View
class SeasonalPricingListView(ListView):
    model = SeasonalPricing
    template_name = 'admin/seasonalpricing_list.html'
    context_object_name = 'seasonal_prices'

    def get_queryset(self):
        return SeasonalPricing.objects.select_related('category').all()

# Update View for Seasonal Pricing
class SeasonalPricingUpdateView(UpdateView):
    model = SeasonalPricing
    form_class = SeasonalPricingForm
    template_name = 'admin/seasonalpricing_form.html'
    success_url = reverse_lazy('category_list')

# Delete View for Seasonal Pricing
class SeasonalPricingDeleteView(DeleteView):
    model = SeasonalPricing
    template_name = 'admin/seasonalpricing_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    

# Create View for Tourist Location
class TouristLocationCreateView(CreateView):
    model = TouristLocation
    form_class = TouristLocationForm
    template_name = 'admin/touristlocation_form.html'
    success_url = reverse_lazy('category_list')

# Update View for Tourist Location
class TouristLocationUpdateView(UpdateView):
    model = TouristLocation
    form_class = TouristLocationForm
    template_name = 'admin/touristlocation_form.html'
    success_url = reverse_lazy('category_list')

# Delete View for Tourist Location
class TouristLocationDeleteView(DeleteView):
    model = TouristLocation
    template_name = 'admin/touristlocation_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    
# Tourist Location List View
class TouristLocationListView(ListView):
    model = TouristLocation
    template_name = 'admin/touristlocation_list.html'
    context_object_name = 'tourist_locations'

    def get_queryset(self):
        return TouristLocation.objects.all()