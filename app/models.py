from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    objects = CustomUserManager()  # Use the custom manager for user creation

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)  # Price for the category
    number_of_rooms = models.PositiveIntegerField(default=0)  # Number of rooms in this category
    is_available = models.BooleanField(default=True)  # Availability of the category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Seasonal Pricing Model (applied per Category)
class SeasonalPricing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='seasonal_prices')
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)  # Override price for the category during this season

    def __str__(self):
        return f"{self.category.name} - {self.price_per_night} (from {self.start_date} to {self.end_date})"


# Tourist Location Model
class TouristLocation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    distance_from_home_stay = models.DecimalField(max_digits=5, decimal_places=2, help_text="Distance in kilometers")
    image = models.ImageField(upload_to='tourist_locations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.room.name} ({self.start_date} to {self.end_date})"

    @property
    def total_price(self):
        seasonal_pricing = SeasonalPricing.objects.filter(
            room=self.room,
            start_date__lte=self.start_date,
            end_date__gte=self.end_date
        ).first()
        price = seasonal_pricing.price_per_night if seasonal_pricing else self.room.price_per_night
        delta = (self.end_date - self.start_date).days
        return delta * price

# Payment Model
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('pending', 'Pending'), ('failed', 'Failed')])
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.booking} - {self.amount} ({self.status})"
