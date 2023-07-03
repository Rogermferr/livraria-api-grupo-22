from rest_framework import generics
from .serializer import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permission import UserCustomPermission


class UserView(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [UserCustomPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer
