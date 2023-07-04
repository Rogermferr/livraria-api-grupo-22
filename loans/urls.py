from django.urls import path

from .views import LoansView, LoansCreateView

urlpatterns = [
    path("loans/", LoansView.as_view()),
    #path("books/<int:pk>/copies/", BookDetailView.as_view()),
    path("loans/copy/<int:pk>/", LoansCreateView.as_view()),

]