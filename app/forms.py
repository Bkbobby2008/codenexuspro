from django import forms  # ✅ Correct import for forms
from .models import Customer  # Ensure models are correctly imported
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm,UsernameField,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm


# LoginForm
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'true', 'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'})
    )

# CustomerRegistrationForm
class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))  # Fixed here

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# MyPasswordchangeForm
class MyPasswordchangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old_Password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'forms-control'}))
    new_password1 = forms.CharField(label='Old_Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'forms-control'}))
    new_password2 = forms.CharField(label='Old_Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'forms-control'}))


# PasswordResetForm
class PasswordResetForm(PasswordChangeForm):
    pass

# MyPasswordResetForm
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label="Email",
        required=True
    )

# Password Change Form 
class MyPasswordChangeForm(PasswordChangeForm):
    pass 


# MySetPasswordForm
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    
# CustomerProfileForm(2)
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'location', 'city', 'mobile', 'state', 'zipcode']
        widgets = {  
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }