
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from .views import ForumsListAPIView, GetForumsbyCategory, GetForumByCategoryAndSlug, UserRegistration, UserLogin


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/forums/', ForumsListAPIView.as_view(), name='api_forums'),
    path('api/v1/forums/<slug:slug>/', GetForumsbyCategory.as_view(), name='api_get_forums'),
    path('api/v1/forums/<slug:category_slug>/<slug:slug>/', GetForumByCategoryAndSlug.as_view(), name='api_forum'),
    path('api/v1/user/registration/', UserRegistration.as_view(), name='signup_api'),
    path('api/v1/user/login/', UserLogin.as_view(), name='api_login')

]