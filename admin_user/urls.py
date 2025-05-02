from django.urls import path
from . import views

app_name = 'admin_user'
urlpatterns = [
    #account
    path('admin_account/', views.EditAccountView.as_view(), name='admin_account'),
    path('admin_account_delete/<int:user_id>/', views.DeleteAccountView.as_view(), name='admin_delete_account'),
    path('admin_account_update/<int:user_id>/', views.UpdateAccountView.as_view(), name='admin_update_account'),
    path('admin_account_add/', views.AddAccountView.as_view(), name='admin_add_account'),
    #product
    path('admin_product/', views.EditProductView.as_view(), name='admin_product'),
    path('admin_product_delete/<int:product_id>/', views.DeleteProductView.as_view(), name='admin_delete_product'),
    path('admin_product_add/', views.AddProductView.as_view(), name='admin_add_product'),
    path('admin_product_update/<int:product_id>/', views.UpdateProductView.as_view(), name='admin_update_product'),
    #category
    path('admin_category/', views.EditCategoryView.as_view(), name='admin_category'),
    path('admin_category_add/', views.AddCategoryView.as_view(), name='admin_add_category'),
    path('admin_category_delete/<int:category_id>/', views.DeleteCategoryView.as_view(), name='admin_delete_category'),
    path('admin_category_update/<int:category_id>/', views.UpdateCategoryView.as_view(), name='admin_update_category'),
    #orders
    path('admin_order/', views.EditOrderView.as_view(), name='admin_order'),
    path('admin_order_delete/<int:order_id>/', views.UpdateOrderView.as_view(), name='admin_update_order'),
    #payment
    path('admin_payment/', views.EditPaymentView.as_view(), name='admin_payment'),
    path('admin_payment_time/<ptime>/', views.EditPaymentTimeView.as_view(), name='admin_payment_time'),
]
