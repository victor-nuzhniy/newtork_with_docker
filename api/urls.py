"""Module for 'api' app urls."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AnaliticView,
    LastLikesView,
    LastPostsView,
    LikeView,
    PostCreateView,
    RegisterView,
    StatisticView,
    UserActivityView,
)

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/signup/", RegisterView.as_view(), name="sign_up"),
    path("post/", PostCreateView.as_view(), name="create_post"),
    path("post/last/", LastPostsView.as_view(), name="last_posts"),
    path("like/", LikeView.as_view(), name="like"),
    path("like/last/", LastLikesView.as_view(), name="last_likes"),
    path("analitics/", AnaliticView.as_view(), name="analitics"),
    path("analitics/activity/<int:pk>/", UserActivityView.as_view(), name="activity"),
    path("analitics/statistic/", StatisticView.as_view(), name="statistic"),
]
