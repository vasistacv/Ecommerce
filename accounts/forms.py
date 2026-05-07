"""Account forms for registration, login, and profile management."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Address


class RegisterForm(UserCreationForm):
    """User registration form with extended fields."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input', 'placeholder': 'Email Address',
            'id': 'register-email'
        })
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input', 'placeholder': 'First Name',
            'id': 'register-firstname'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input', 'placeholder': 'Last Name',
            'id': 'register-lastname'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Username',
                'id': 'register-username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-input', 'placeholder': 'Password',
            'id': 'register-password1'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-input', 'placeholder': 'Confirm Password',
            'id': 'register-password2'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class LoginForm(AuthenticationForm):
    """Custom login form with styled widgets."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Username or Email',
        'id': 'login-username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Password',
        'id': 'login-password'
    }))


class ProfileForm(forms.ModelForm):
    """User profile edit form."""
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-input', 'id': 'profile-firstname'
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-input', 'id': 'profile-lastname'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 'id': 'profile-email'
    }))

    class Meta:
        model = UserProfile
        fields = ['phone', 'date_of_birth', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'id': 'profile-phone'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input', 'type': 'date', 'id': 'profile-dob'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3, 'id': 'profile-bio'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-input', 'id': 'profile-avatar'}),
        }


class AddressForm(forms.ModelForm):
    """Shipping/billing address form."""
    class Meta:
        model = Address
        fields = ['address_type', 'full_name', 'street_address', 'apartment',
                  'city', 'state', 'zip_code', 'country', 'phone', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-input', 'id': 'address-type'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name', 'id': 'address-name'}),
            'street_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street Address', 'id': 'address-street'}),
            'apartment': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apartment, Suite (optional)', 'id': 'address-apt'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City', 'id': 'address-city'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State', 'id': 'address-state'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ZIP Code', 'id': 'address-zip'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Country', 'id': 'address-country'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone', 'id': 'address-phone'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-checkbox', 'id': 'address-default'}),
        }
