from django.shortcuts import render, redirect
from django.views import View
from account.models import User
from django.contrib import messages
from .forms import UpdateAccountForm, AddACountForm, AddCategoryForm, UpdateCategoryForm, UpdateProductForm, \
    UpdateOrderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Category, Product
from orders.models import OrdersModel, PaymentModel
import time


# -----Account-----
class EditAccountView(LoginRequiredMixin, View):

    def get(self, request):
        users = User.object.all()
        return render(request, 'admin_user/EditAccount.html', {'users': users})


class DeleteAccountView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.object.get(id=user_id)
        user.delete()
        users = User.object.all()
        return render(request, 'admin_user/EditAccount.html', {'users': users})


class UpdateAccountView(LoginRequiredMixin, View):
    form_class = UpdateAccountForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = User.object.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, user_id):
        user = self.user_instance
        form = self.form_class(instance=user)
        return render(request, 'admin_user/UpdateAccount.html', {'form': form})

    def post(self, request, user_id):
        user = self.user_instance
        form = self.form_class(request.POST, instance=user)
        if form.is_valid:
            form.save()
            users = User.object.all()
            return render(request, 'admin_user/EditAccount.html', {'users': users})


class AddAccountView(LoginRequiredMixin, View):
    form_class = AddACountForm
    template_name = 'admin_user/AddAccount.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(phone_number=cd['phone_number'], email=cd['email'],
                        full_name=cd['full_name'],
                        password=cd['password'])
            if cd['is_admin']:
                user.is_admin = True
            user.save()
            users = User.object.all()
            return render(request, 'admin_user/EditAccount.html', {'users': users})
        return render(request, self.template_name, {'form': form})


# -----Product-----
class EditProductView(LoginRequiredMixin, View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'admin_user/EditProducts.html', {'products': products})


class DeleteProductView(LoginRequiredMixin, View):

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        products = Product.objects.all()
        return render(request, 'admin_user/EditProducts.html', {'products': products})


class UpdateProductView(LoginRequiredMixin, View):
    form_class = UpdateProductForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = Product.objects.get(pk=kwargs['product_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product_instance
        form = self.form_class(instance=product)
        return render(request, 'admin_user/UpdateProduct.html', {'form': form})

    def post(self, request, *args, **kwargs):
        product = self.product_instance
        form = self.form_class(request.POST, request.FILES, instance=product)
        if form.is_valid:
            form.save(commit=False)
            form.image = request.FILES['image']
            form.save()
            products = Product.objects.all()
            return render(request, 'admin_user/EditProducts.html', {'products': products})


class AddProductView(LoginRequiredMixin, View):
    form_class = UpdateProductForm
    template_name = 'admin_user/AddProduct.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            form.save(commit=False)
            form.image = request.FILES['image']
            form.save()
            products = Product.objects.all()
            return render(request, 'admin_user/EditProducts.html', {'products': products})
        return render(request, self.template_name, {'form': form})


# -----Category-----
class EditCategoryView(LoginRequiredMixin, View):

    def get(self, request):
        categorys = Category.objects.all()
        return render(request, 'admin_user/EditCategory.html', {'categorys': categorys})


class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        category.delete()
        categorys = Category.objects.all()
        return render(request, 'admin_user/EditCategory.html', {'categorys': categorys})


class UpdateCategoryView(LoginRequiredMixin, View):
    form_class = UpdateCategoryForm

    def setup(self, request, *args, **kwargs):
        self.category_instance = Category.objects.get(pk=kwargs['category_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        category = self.category_instance
        form = self.form_class(instance=category)
        return render(request, 'admin_user/UpdateCategory.html', {'form': form})

    def post(self, request, *args, **kwargs):
        category = self.category_instance
        form = self.form_class(request.POST, instance=category)
        if form.is_valid:
            form.save()
            categorys = Category.objects.all()
            return render(request, 'admin_user/EditCategory.html', {'categorys': categorys})


class AddCategoryView(LoginRequiredMixin, View):
    form_class = AddCategoryForm
    template_name = 'admin_user/AddCategory.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            category = Category(name=cd['name'], slug=cd['slug'])
            category.save()
            categorys = Category.objects.all()
            return render(request, 'admin_user/EditCategory.html', {'categorys': categorys})


# -----Order-----
class EditOrderView(LoginRequiredMixin, View):
    def get(self, request):
        orders = OrdersModel.objects.all()
        orders = orders.order_by('-order_date_update')
        return render(request, 'admin_user/EditOrder.html', {'orders': orders})


class UpdateOrderView(LoginRequiredMixin, View):
    form_class = UpdateOrderForm

    def get(self, request, order_id):
        form = self.form_class()
        OrdersModel.objects.get(pk=order_id)
        return render(request, 'admin_user/UpdateOrder.html', {'form': form})

    def post(self, request, order_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order_model = OrdersModel.objects.get(pk=order_id)
            order_model.order_statues = cd['order_statues']
            order_model.save()
            orders = OrdersModel.objects.all()
            return render(request, 'admin_user/EditOrder.html', {'orders': orders})


# -----payment-----
class EditPaymentView(LoginRequiredMixin, View):

    def get(self, request):
        payments = PaymentModel.objects.all()
        return render(request, 'admin_user/EditPayment.html', {'payments': payments})

    def post(self, request):
        payments = PaymentModel.objects.all()
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        if from_date:
            payments = payments.filter(date__range=(from_date, to_date))
        else:
            messages.error(request, 'یک تاریخ را انتخاب کنید', 'danger')
        return render(request, 'admin_user/EditPayment.html', {'payments': payments})


class EditPaymentTimeView(LoginRequiredMixin, View):
    def get(self, request, ptime):
        payments = PaymentModel.objects.all()
        if ptime == 'new':
            payments = payments.order_by('-date')
        elif ptime == 'old':
            payments = payments.order_by('date')
        elif ptime == 'hour_ego':
            hour = time.localtime()
            payments = payments.filter(date__hour=hour.tm_hour - 5, date__day=time.localtime().tm_mday)
        elif ptime == 'day_ego':
            day = time.localtime()
            payments = payments.filter(date__day=day.tm_mday, date__month=time.localtime().tm_mon)
        elif ptime == 'month_ego':
            month = time.localtime()
            payments = payments.filter(date__month=month.tm_mon)

        return render(request, 'admin_user/EditPayment.html', {'payments': payments})
