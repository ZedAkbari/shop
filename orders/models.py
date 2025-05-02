from django.db import models
from home.models import Product
from account.models import User


class ShopBasket(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sproduct')
    count_pro = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user_id} add --{self.count_pro}-- of ----{self.product}----'


class OrdersModel(models.Model):
    pay = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ouser')
    total_price = models.IntegerField()
    tracking_code = models.IntegerField(default=None)
    order_statues = models.CharField(max_length=300, choices=[
        ('در حال پردازش', 'در حال پردازش'),
        ('در حال ارسال به مقصد', 'در حال ارسال به مقصد'),
        ('تحویل داده شده', 'تحویل داده شده')
    ], default='در حال پردازش')
    order_date_update = models.DateTimeField(auto_now=True)
    order_date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name} _ {self.tracking_code} _ {self.order_statues}'


class OrdersInterface(models.Model):
    order = models.ForeignKey(OrdersModel, on_delete=models.CASCADE, related_name='border')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bproduct')
    count_pro = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return f'{self.order.id} _ {self.product.name}'


class PaymentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrdersModel, on_delete=models.CASCADE)
    statues_code = models.IntegerField(default=None)
    tracking_code = models.IntegerField(default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name} _ {self.order.id} _ {self.statues_code}'
