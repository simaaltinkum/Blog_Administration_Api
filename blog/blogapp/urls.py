from django.urls import path
from .views import UserView, UserProfileView, BlogView, BlogDetailView

urlpatterns = [
    path('auth/register/', UserView.as_view(), {'action': 'register'}, name='register'),
    path('auth/login/', UserView.as_view(), {'action': 'login'}, name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('blogs/', BlogView.as_view(), name='blogs'),
    path('blogs/<int:id>/', BlogDetailView.as_view(), name='blogs')
]