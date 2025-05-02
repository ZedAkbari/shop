from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('detail/<int:pro_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<category_name>/', views.ProductCategoryView.as_view(), name='product_category'),
    path('max_price/', views.ProductMaxPriceView.as_view(), name='max_price'),
    path('min_price/', views.ProductMinPriceView.as_view(), name='min_price'),
]
