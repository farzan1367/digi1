from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm
from django import forms
from .models import Profile

class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'تلفن'}),
        required=False
    )   
    adress1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'آدرس اول'}),
        required=False
    )    
    adress2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'آدرس دوم'}),
        required=False
    )  
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شهر'}),
        required=False
    )  
    state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'منطقه'}),
        required=False
    )  
    zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کدپستی'}),
        required=False
    )  
    country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کشور'}),
        required=False
    )  


    class Meta:
        model = Profile
        fields =('phone','adress1','adress2','city','state','zipcode','country')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خود را وارد کنید'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خانوادگی خود را وارد کنید'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل خود را وارد کنید'})
    )
    username = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری خود را وارد کنید'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خود شامل 8 کاراکتر و فقط عدد نباشد را وارد کنید'
            }
        )
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خود را تکرار کنید'
            }
        )
    )

    class Meta():
        model = User
        fields=('first_name','last_name','email','username','password1','password2')

class UpdateUserForm(UserChangeForm):
    password = None
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خود را وارد کنید'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خانوادگی خود را وارد کنید'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل خود را وارد کنید'})
    )
    username = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری خود را وارد کنید'})
    )

    class Meta():
        model = User
        fields=('first_name','last_name','email','username',)    


class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خود شامل 8 کاراکتر و فقط عدد نباشد را وارد کنید'
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خود را تکرار کنید'
            }
        )
    )

    class Meta:
        model = User
        fields =('new_passwor1','new_password2')
