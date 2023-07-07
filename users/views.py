from rest_framework import generics
from .serializer import UserSerializer, UserFollowerSerializer
from .models import User
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permission import UserCustomPermission
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status


class UserView(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [UserCustomPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewfollowerBook(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserFollowerSerializer

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs['book_id'])
        user = self.request.user
        
        if not book:
            raise NotFound({"error": "Livro não encontrado"})
        
        book.follower.add(user)
        book.save()

        return Response({"message": f"Você esta seguindo o {book.title}"}, 
                        status=status.HTTP_201_CREATED)
         

     