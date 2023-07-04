from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from books.permissions import IsAdminOrReadOnly
from copies.models import Copy
from loans.models import Loan
from users.models import User
from loans.permissions import IsAdminOrOwner
from loans.serializers import LoanSerializer
from users.permission import UserCustomPermission
from rest_framework.permissions import IsAuthenticated

...


class LoansView(generics.ListAPIView):
    permission_classes = [IsAdminOrOwner, IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self.queryset = Loan.objects.filter(user=request.user)

        self.queryset = Loan.objects.all()

        return self.list(request, *args, **kwargs)


class LoansCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()

    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        user = User.objects.filter(id=self.request.data.get("user_id")).first()
        copy = Copy.objects.filter(id=self.kwargs.get("pk")).first()
        return serializer.save(copy=copy, user=user)
