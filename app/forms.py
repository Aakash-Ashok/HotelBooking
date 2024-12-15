# forms.py

from django import forms
from .models import *
from django.utils import timezone

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class CategoryForm(forms.ModelForm):
    IS_AVAILABLE_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    # Use BooleanField for is_available with RadioSelect widget for Yes/No options
    is_available = forms.ChoiceField(
        choices=IS_AVAILABLE_CHOICES,
        widget=forms.RadioSelect,
        label="Is the Category Available?"
    )
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'price_per_night', 'number_of_rooms', 'is_available','image']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class SeasonalPricingForm(forms.ModelForm):
    class Meta:
        model = SeasonalPricing
        fields = ['category', 'start_date', 'end_date', 'price_per_night']
        
        widgets={
           'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class TouristLocationForm(forms.ModelForm):
    class Meta:
        model = TouristLocation
        fields = ['name', 'description', 'distance_from_home_stay', 'image']
        
        
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']  # Fields to include in the form
        

class BookingForm(forms.ModelForm):
    # Non-DB Fields
    name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    special_requests = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests...'}),
        label="Special Requests"
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('bank_transfer', 'Bank Transfer'),
            ('debit_card','Debit Card'),
            ('cash','Cash')
        ],
        label="Payment Method"
    )
    number_of_guests = forms.IntegerField(min_value=1, label="Number of Guests")

    class Meta:
        model = Booking
        fields = ['Category', 'start_date', 'end_date']  # Fields to save in DB

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('Category')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Validate booking dates
        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past.")
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after the start date.")
        
        # Validate room availability
        if category and category.number_of_rooms <= 0:
            raise forms.ValidationError(f"No rooms available in the '{category.name}' category.")
        if category and not category.is_available:
            raise forms.ValidationError(f"The '{category.name}' category is currently unavailable.")

        return cleaned_data