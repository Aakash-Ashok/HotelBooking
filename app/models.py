from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.



class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("customer", "Customer"),
    ]
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default="customer")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(
        upload_to="static/images/admin_profile",
        default='static/images/admin_profile/default.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Admin Profile: {self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="static/images/customer_profile",
        default='static/images/customer_profile/default.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Customer Profile: {self.user.username}"
