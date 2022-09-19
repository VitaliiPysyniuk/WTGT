from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserListView, UserRegisterView, UserUpdateView

urlpatterns = [
    path('', UserListView.as_view(), name='get_all_users'),
    path('/register', UserRegisterView.as_view(), name='register_new_user'),
    path('/<int:id>', UserUpdateView.as_view(), name='update_single_user'),
    path('/login', TokenObtainPairView.as_view(), name='get_token_pair'),
    path('/refresh', TokenRefreshView.as_view(), name='refresh_access_token'),
]
