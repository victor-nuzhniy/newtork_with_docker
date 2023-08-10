"""Module for 'api' app urls."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LikeView, PostCreateView, RegisterView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("signup/", RegisterView.as_view(), name="sign_up"),
    path("post/", PostCreateView.as_view(), name="create_post"),
    path("like/", LikeView.as_view(), name="like"),
]
