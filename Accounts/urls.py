from django.urls import path
from .views import UserListCreateAPIView,UserLoginView

urlpatterns = [
    path('register/', UserListCreateAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
