from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RegisteredCustomer, RegisteredAddress

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = RegisteredCustomer
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 
                  'date_of_birth', 'password1', 'password2')

class AddressForm(forms.ModelForm):
    class Meta:
        model = RegisteredAddress
        fields = ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 
                  'country', 'is_default')
        widgets = {
            'address_line2': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }
