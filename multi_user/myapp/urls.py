from django.urls import path
from .views import *
from .forms import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',home, name='home'),
    path('cust_register/',cust_registration, name='cust_register'),
    path('emp_register/',emp_registration, name='emp_register'),
    path('login/',login_func, name='login'),
    path('emp_profile/',emp_profile, name='emp_profile'),
    path('admin_page/',admin_page, name='admin_page'),
    path('logout/',logout_func, name='logout'),

    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='authenticate/passwordchange.html', form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='authenticate/passwordchangedone.html'),name='passwordchangedone'),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='authenticate/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='authenticate/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='authenticate/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='authenticate/password_reset_complete.html'),name='password_reset_complete'),
]