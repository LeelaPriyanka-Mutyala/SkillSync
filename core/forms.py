from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SkillListing, SwapRequest

class ListingForm(forms.ModelForm):
    class Meta:
        model = SkillListing
        fields = ['title', 'description', 'category', 'listing_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RequestForm(forms.ModelForm):
    class Meta:
        model = SwapRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Hi! I saw your listing and...'}),
        }

# ✅ NEW: Registration Form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })