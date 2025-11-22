from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Enquiry, Appointment  # ← NEW IMPORT

class RegisterForm(UserCreationForm):
    """Custom registration form with additional fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })
        
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Custom login form with styled fields"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


# ============================================
# NEW: ENQUIRY FORM FOR LANDING PAGE
# ============================================
class EnquiryForm(forms.ModelForm):
    """Form for tattoo enquiries from landing page"""
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message', 'preferred_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your tattoo idea...',
                'rows': 5,
                'required': True,
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
            }),
        }


class AppointmentForm(forms.ModelForm):
    """Client appointment booking form"""

    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Appointment
        fields = ['client_name', 'email', 'phone', 'tattoo_design', 'appointment_date', 'reference_image']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'tattoo_design': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your design idea'}),
            'reference_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AppointmentStatusForm(forms.ModelForm):
    """Admin status update form"""

    class Meta:
        model = Appointment
        fields = ['status']