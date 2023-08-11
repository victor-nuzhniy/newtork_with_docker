"""Module for 'api' app urls."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AnaliticView,
    LikeView,
    PostCreateView,
    RegisterView,
    StatisticView,
    UserActivityView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("signup/", RegisterView.as_view(), name="sign_up"),
    path("post/", PostCreateView.as_view(), name="create_post"),
    path("like/", LikeView.as_view(), name="like"),
    path("analitics/", AnaliticView.as_view(), name="analitics"),
    path("activity/<int:pk>/", UserActivityView.as_view(), name="activity"),
    path("statistic/", StatisticView.as_view(), name="statistic"),
]
