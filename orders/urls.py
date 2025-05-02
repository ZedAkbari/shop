from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('shopping_basket/<int:user_id>/', views.ShoppingBasket.as_view(), name='shopping_basket'),
    path('remove_basket/<int:pro_id>/', views.BasketRemoveView.as_view(), name='basket_remove'),
    path('orders_info/', views.OrdersInfoView.as_view(), name='orders_info'),
    path('order_info/<int:order_id>/', views.ExistsOrderInfoView.as_view(), name='exists_order_info'),
    path('user_order/<int:user_id>/', views.UserOrderView.as_view(), name='user_order'),
    path('pay/<int:order_id>/', views.OrdersPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    path('order_products/<int:order_id>/', views.OrderProductView.as_view(), name='order_product'),
    path('payment_user/<int:user_id>/', views.PaymentUserView.as_view(), name='payment_user'),
    path('payment_order/<int:order_id>/', views.PaymentOrderView.as_view(), name='payment_order'),
]
