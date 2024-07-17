from django.urls import path
from .views import user_login, signup, logout_view, ForumView, read_and_write

urlpatterns = [
    path('user/login/', user_login, name='user_login'),
    path('user/signup/', signup, name='user_signup'),
    path('user/logout/', logout_view, name='user_logout'),
    path('use/<slug:forum_slug>/', ForumView, name='forum_view'),
    path('use/<slug:category_slug>/<slug:forum_slug>/', read_and_write, name='forum_read')
]