from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from accounts.models import User
from e_store.models import Address

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=30, help_text="Required: Add a valid email address")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'mobile', 'password1', 'password2']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'region', 'province', 'city', 'brgy_dist_name','postal_code', 'detailed_address']



class LoginUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")


    
