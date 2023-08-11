"""Module for 'api' app urls."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AnaliticView,
    LastPostsView,
    LikeView,
    PostCreateView,
    RegisterView,
    StatisticView,
    UserActivityView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterView.as_view(), name="sign_up"),
    path("post/", PostCreateView.as_view(), name="create_post"),
    path("like/", LikeView.as_view(), name="like"),
    path("analitics/", AnaliticView.as_view(), name="analitics"),
    path("activity/<int:pk>/", UserActivityView.as_view(), name="activity"),
    path("statistic/", StatisticView.as_view(), name="statistic"),
    path("post/last/", LastPostsView.as_view(), name="last_posts"),
]
