from django.contrib import admin
from .models import ShopBasket, OrdersModel, OrdersInterface, PaymentModel


admin.site.register(ShopBasket)
admin.site.register(OrdersModel)
admin.site.register(OrdersInterface)
admin.site.register(PaymentModel)
