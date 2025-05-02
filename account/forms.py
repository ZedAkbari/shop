from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and ['password1'] != ['password2']:
            raise ValidationError('the password and confirm password is not match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11, label='شماره تلفن')
    full_name = forms.CharField(label="نام و نام خانوادگی")
    email = forms.EmailField(label="ایمیل")
    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, label='شماره تلفن')
    password = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)


class UserChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number')


class UserInfoCreatForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput, label='آدرس')
