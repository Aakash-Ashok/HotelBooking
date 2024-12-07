# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView , TemplateView
from .forms import CustomerRegistrationForm
from .models import User
from django.contrib.auth import authenticate, login

class IndexView(TemplateView):
    template_name="index.html"
    
    
class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')  # Redirect after successful registration

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Hash the password
        user.role = 'customer'  # Set the role to 'customer'
        user.save()
        login(self.request, user)  # Log the user in automatically after registration
        messages.success(self.request, 'Registration successful.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your registration.')
        return super().form_invalid(form)


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
            messages.success(request, 'You have been logged in successfully.')
            return redirect('home')  # Redirect to home page (you can change this as needed)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)  # Re-render the login form with error message
        

