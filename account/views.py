from django.shortcuts import render, redirect
from django.views import View
from .models import User, UserInfo
from .forms import UserRegisterForm, UserLoginForm, UserChangeProfileForm, UserInfoCreatForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from admin_user.forms import UpdateAccountForm


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.object.create_user(cd['phone_number'], cd['email'], cd['full_name'], cd['password'])
            messages.success(request, "ثبت نام شما با موفقیت انجام شد", 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        print("=========get", form)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
            messages.error(request, "نام کاربری یا گذرواژه نادرست است", 'danger')
            return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.object.get(pk=user_id)
        return render(request, 'account/profile.html', {'user': user})

    def post(self, request, user_id):
        user = User.object.get(pk=user_id)
        return render(request, 'account/profile.html', {'user': user})


class UserChangeProfileView(LoginRequiredMixin, View):
    form_class = UserChangeProfileForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = User.object.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, user_id):
        user = self.user_instance
        form = self.form_class(instance=user)
        return render(request, 'account/change_profile.html', {'form': form})

    def post(self, request, user_id):
        user = self.user_instance
        form = self.form_class(request.POST, instance=user)
        if form.is_valid:
            form.save()
            user = user
            return render(request, 'account/profile.html', {'user': user})


class CreateUserInfo(LoginRequiredMixin, View):
    form_class = UserInfoCreatForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'orders/PayTemplate.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_info = UserInfo.objects.filter(user=request.user, address=cd['address'])
            if not user_info.exists():
                UserInfo.objects.create(user=request.user, address=cd['address'])
                return render(request, 'orders/PayTemplate.html')
            return render(request, 'orders/PayTemplate.html')
