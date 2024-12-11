# forms.py

from django import forms
from .models import *

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
        fields = ['name', 'description', 'price_per_night', 'number_of_rooms', 'is_available']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class SeasonalPricingForm(forms.ModelForm):
    class Meta:
        model = SeasonalPricing
        fields = ['category', 'start_date', 'end_date', 'price_per_night']

class TouristLocationForm(forms.ModelForm):
    class Meta:
        model = TouristLocation
        fields = ['name', 'description', 'distance_from_home_stay', 'image']