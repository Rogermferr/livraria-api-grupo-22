from django.urls import path

from .views import LoansView, LoansCreateView, LoansUpdateView

urlpatterns = [
    path("loans/", LoansView.as_view()),
    path("loans/copy/<int:pk>/", LoansCreateView.as_view()),
    path("loans/copy/<int:pk>/update/", LoansUpdateView.as_view()),
]
