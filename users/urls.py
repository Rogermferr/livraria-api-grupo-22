from django.urls import path
from .views import UserView, UserViewfollowerBook
from rest_framework_simplejwt import views

urlpatterns = [
    path('users/', UserView.as_view()),
    path('login/', views.TokenObtainPairView.as_view()),
    path('users/follower/<int:book_id>', UserViewfollowerBook.as_view())
]
