from django.shortcuts import render, redirect
from django.views import View
from .models import Product, ProductCountView
from django.contrib import messages
from .forms import ProductSearchForm
from orders.forms import CartAddForm
import socket, base64
from orders.models import ShopBasket


class HomeView(View):

    def get(self, request):
        products = Product.objects.all()
        for product in products:
            pro_view = ProductCountView.objects.filter(product=product)
            pro_view = pro_view.count()
            product.view = pro_view
            product.save()
        products = products.order_by('-view')
        p = products.last()
        encoded_data = base64.b64encode(str(p.image).encode())
        return render(request, 'home/home.html', {'products': products, 'a': encoded_data})


class ProductView(View):
    def get(self, request):
        form = ProductSearchForm()
        products = Product.objects.filter(available=True)
        if 'search' in request.GET:
            form = ProductSearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                products = products.filter(name__icontains=cd, slug__icontains=cd)
        return render(request, "home/products.html", {'products': products, 'form': form})


class ProductDetailView(View):

    def get(self, request, pro_id):
        form = CartAddForm()
        product = Product.objects.get(pk=pro_id)
        if request.user.is_authenticated:
            host_name = socket.gethostname()
            ip = socket.gethostbyname(host_name)
            product_view = ProductCountView.objects.filter(product=product, user=ip)
            if not product_view.exists():
                count_view = ProductCountView(product=product, user=ip)
                count_view.save()
        return render(request, 'home/detail.html', {'product': product, 'form': form})

    def post(self, request, pro_id):
        product = Product.objects.get(pk=pro_id)
        form = CartAddForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            count_pro = cd['quantity']
            total_price = count_pro * product.price
            shop_basket = ShopBasket.objects.filter(user_id=request.user.id, product=product)
            if shop_basket.exists():
                if form.is_valid():
                    cd = form.cleaned_data
                    count_pro = cd['quantity']
                    basket_products = ShopBasket.objects.filter(product=product)
                    for basket_product in basket_products:
                        basket_product.count_pro = count_pro
                        basket_product.total_price = count_pro * product.price
                        basket_product.save()
                        if basket_product.count_pro == 0:
                            basket_product.delete()
                baskets = ShopBasket.objects.filter(user_id=request.user.id)
                return render(request, 'orders/ShopBasketTemplate.html', {'baskets': baskets})
            ShopBasket.objects.create(user_id=request.user.id, product=product, count_pro=count_pro,
                                      total_price=total_price)
            baskets = ShopBasket.objects.filter(user_id=request.user.id)
            return render(request, 'orders/ShopBasketTemplate.html', {'baskets': baskets})


class ProductCategoryView(View):

    def get(self, request, category_name):
        products = Product.objects.filter(category__name=category_name)
        form = ProductSearchForm()
        if 'search' in request.GET:
            products = Product.objects.filter(available=True)
            form = ProductSearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                products = products.filter(name__icontains=cd, slug__icontains=cd)
        return render(request, 'home/products.html', {'products': products, 'form': form})


class ProductMaxPriceView(View):

    def get(self, request):
        products = Product.objects.filter(available=True)
        products = products.order_by('-price')
        form = ProductSearchForm()
        if 'search' in request.GET:
            form = ProductSearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                products = products.filter(name__icontains=cd, slug__icontains=cd)
        return render(request, 'home/products.html', {'products': products, 'form': form})


class ProductMinPriceView(View):

    def get(self, request):
        products = Product.objects.filter(available=True)
        products = products.order_by('price')
        form = ProductSearchForm()
        if 'search' in request.GET:
            form = ProductSearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                products = products.filter(name__icontains=cd, slug__icontains=cd)
        return render(request, 'home/products.html', {'products': products, 'form': form})
