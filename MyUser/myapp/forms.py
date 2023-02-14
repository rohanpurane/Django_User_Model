from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=80)
    class Meta:
        model = MyUser
        fields = ('email', 'username', 'password1', 'password2')
 
class LoginForm(forms.ModelForm):
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'placeholder':'Password', 'class':'form-control'}))
    class Meta:
        model = MyUser
        fields = ('email','password')
        

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old_Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus': True, 'placeholder':'Old Password', 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New_Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'placeholder':'New Password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("New_Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'placeholder':'Confirm New Password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'placeholder':'Registered Email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
        new_password1 = forms.CharField(label=_("New_Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'placeholder':'New Password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
        new_password2 = forms.CharField(label=_("Confirm_New_Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'placeholder':'Confirm New Password', 'class':'form-control'}))
