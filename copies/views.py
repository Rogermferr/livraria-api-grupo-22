from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import CopySerializer
from books.models import Book


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    queryset = Book.objects.all()
    serializer_class = CopySerializer
