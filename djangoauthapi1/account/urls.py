from django.urls import path
from account.views import UserRegistrationView,LoginView,UserProfileView,PasswordChangeView

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile-info/',UserProfileView.as_view(),name='profile-info'),
    path('change-password/',PasswordChangeView.as_view(),name='change-password'),
    # path('logout/',LogoutView.as_view(),name='logout'),
]