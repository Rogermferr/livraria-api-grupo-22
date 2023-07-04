from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import CopySerializer
from .models import Copy
from books.permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from books.models import Book


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    serializer_class = CopySerializer
    queryset = Copy.objects.all()


class CopyCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = CopySerializer

    def get_queryset(self):
        book_id = self.kwargs.get("pk")
        return Copy.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book_id = self.kwargs.get("pk")
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(book=book)
