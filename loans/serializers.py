from rest_framework import serializers
from copies.serializer import CopySerializer
from users.serializer import UserSerializer
from datetime import timedelta, datetime
from .models import Loan
from rest_framework.exceptions import ValidationError
from rest_framework.views import status


class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    copy = CopySerializer(required=False)

    class Meta:
        model = Loan
        fields = ["id", "created_at", "updated_at", "is_finished", "return_date", "user", "copy"]
        extra_kwargs = {"return_date": {"read_only": True}}

    def create(self, validated_data):
        current_date = datetime.now().date()
        future_date = current_date + timedelta(days=7)

        loan = Loan.objects.filter(user=validated_data.get("user")).first()

        if current_date < loan.return_date and not loan.is_finished:
            raise ValidationError(
                detail={"error": "O empréstimo não pode ser criado."}, code=status.HTTP_401_UNAUTHORIZED
            )

        return Loan.objects.create(return_date=future_date, **validated_data)
