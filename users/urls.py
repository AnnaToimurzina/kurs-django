from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ConfirmationSentView, EmailConfirmedView, \
    EmailConfirmationFailedView, ProfileView, ConfirmEmailView

app_name = UsersConfig.name
urlpatterns = [
    # Main Url
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    # Log Out Url
    path('logout/', LogoutView.as_view(), name='logout'),

    # Registration Url
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),

    # Email Confirmation Urls
    path('email_confirmation_sent/', ConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmation_failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    # Profile Url
    path('profile/', ProfileView.as_view(), name='profile'),

    # Password Reset Urls
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/reset_password/password_reset.html',
             success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/reset_password/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/reset_password/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/reset_password/password_reset_complete.html'),
         name='password_reset_complete'),

]