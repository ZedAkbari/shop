from django import forms
from account.models import User
from home.models import Product, Category
from orders.models import OrdersModel


class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'is_admin')


class AddACountForm(forms.Form):
    full_name = forms.CharField(label='نام و نام خانوادگی')
    email = forms.EmailField(label='ایمیل')
    phone_number = forms.CharField(max_length=11, label='شماره تلفن همراه')
    password = forms.CharField(widget=forms.PasswordInput, label='گذرواژه')
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='ادمین')


class AddCategoryForm(forms.Form):
    name = forms.CharField()
    slug = forms.CharField()


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'slug', 'description', 'price', 'image')


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = OrdersModel
        fields = ('order_statues',)



