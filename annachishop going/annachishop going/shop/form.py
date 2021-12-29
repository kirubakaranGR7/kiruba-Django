from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import User, ShopRegister, Products


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'is_customer',
                  'is_vendor', ]


class ShopRegisterForm(forms.Form):
    name = forms.CharField(max_length=200)
    shop_name = forms.CharField(max_length=200)
    shop_location = forms.CharField(max_length=200)
    Shop_description = forms.CharField(max_length=200)
    mobile_number = forms.IntegerField()

    class Meta:
        model = ShopRegister
        fields = [
            'name', 'shop_name', 'shop_location',
            'Shop_description', 'mobile_number'
        ]


# class AddProductsForm(forms.Form):
#     name = forms.CharField(max_length=250)
#     brand = forms.CharField(max_length=250)
#     description = forms.CharField(max_length=500)
#     price = forms.DecimalField()
#     quantity = forms.IntegerField()
#     created = forms.DateTimeField()
#     modified = forms.DateTimeField()

# class AddProductForm(forms.ModelForm):
#     class Meta:
#         model = Products
#         fields =
