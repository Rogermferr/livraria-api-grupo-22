from django.urls import path
from .views import CopyView, CopyCreateView

urlpatterns = [
    path("copies/", CopyView.as_view()),
    path("copies/books/<int:pk>/", CopyCreateView.as_view()),
]
