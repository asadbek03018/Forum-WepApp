from django.urls import path
from .views import blocked
urlpatterns = [
    path('suspended/user/blocked/', blocked, name='block_template')
]