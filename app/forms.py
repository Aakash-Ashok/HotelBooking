from django import forms
from .models import User, AdminProfile , CustomerProfile

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    department = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder": "Department"}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "Phone Number"}))
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = "admin"
        user.is_staff = True
        if commit:
            user.save()

            # Save AdminProfile
            AdminProfile.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                phone=self.cleaned_data['phone'],
                profile_pic=self.cleaned_data.get('profile_pic', None)
            )
        return user



class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={"placeholder": "Address", "rows": 3}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "Phone Number"}))
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={"placeholder": "Date of Birth", "type": "date"}))
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = "customer"
        if commit:
            user.save()

            # Save CustomerProfile
            CustomerProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone'],
                dob=self.cleaned_data.get('dob', None),
                profile_pic=self.cleaned_data.get('profile_pic', None)
            )
        return user

