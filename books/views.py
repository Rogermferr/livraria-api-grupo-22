from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import BookSerializer, BookUpdateSerializer
from .models import Book
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookUpdateSerializer
