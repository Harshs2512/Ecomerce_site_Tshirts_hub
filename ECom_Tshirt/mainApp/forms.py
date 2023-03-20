from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer

attrs_dict = {'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}

CustomerAdd = {'class': 'sdf'}


class RegistrationForm(UserCreationForm):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=('username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                             label=('email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=('password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=('password (again)'))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name': forms.TextInput(attrs={'class': "form-control"}),
                   'locality': forms.TextInput(attrs={'class': "form-control"}),
                   'city': forms.TextInput(attrs={'class': "form-control"}),
                   'state': forms.Select(attrs={'class': "form-control"}),
                   'zipcode': forms.NumberInput(attrs={'class': "form-control"})}


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['country']
        widgets = {'country': forms.Select(attrs={'class': "form-control"})}
