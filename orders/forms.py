from django import forms
from orders.models import ShopBasket


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, max_value=9, label='')


class BasketAddCountForm(forms.ModelForm):
    count_product = forms.IntegerField(min_value=1, max_value=9, label='')
