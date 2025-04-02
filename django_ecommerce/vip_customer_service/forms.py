from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import VIPCustomer, VIPAddress

class VIPCustomerForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = VIPCustomer
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 
                  'date_of_birth', 'password1', 'password2')

class VIPAddressForm(forms.ModelForm):
    class Meta:
        model = VIPAddress
        fields = ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 
                  'country', 'is_default')
        widgets = {
            'address_line2': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }

class VIPTierUpgradeForm(forms.ModelForm):
    confirm = forms.BooleanField(required=True, label="I understand this will change my VIP tier")
    
    class Meta:
        model = VIPCustomer
        fields = ('vip_tier',)
        widgets = {
            'vip_tier': forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Limit tier options based on current tier
            current_tier = user.vip_tier
            tier_order = ['bronze', 'silver', 'gold', 'platinum']
            current_index = tier_order.index(current_tier)
            
            # Only show tiers higher than current
            available_tiers = [(tier, dict(VIPCustomer.VIP_TIERS)[tier]) 
                              for tier in tier_order[current_index+1:]]
            
            if available_tiers:
                self.fields['vip_tier'].choices = available_tiers
            else:
                self.fields['vip_tier'].choices = [('platinum', 'Platinum')]
                self.fields['vip_tier'].help_text = "You are already at the highest tier." 