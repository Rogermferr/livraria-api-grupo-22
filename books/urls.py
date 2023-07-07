from django.urls import path
from .views import BookView, BookDetailView

urlpatterns = [
    path("books/copies/", BookView.as_view()),
    path("books/<int:pk>/copies/", BookDetailView.as_view()),
]
