from rest_framework import serializers
from copies.serializer import CopySerializer
from users.serializer import UserSerializer
from datetime import timedelta, datetime
from .models import Loan
from rest_framework.exceptions import ValidationError
from copies.models import Copy
from django.shortcuts import get_object_or_404


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

        copy_id = self.context["view"].kwargs["pk"]
        copy = get_object_or_404(Copy, id=copy_id)

        if not copy.is_available:
            raise ValidationError(detail={"error": "Essa cópia não está disponível."})

        if current_date > loan.return_date and not loan.is_finished:
            raise ValidationError(detail={"error": "O empréstimo não pode ser criado."})

        if future_date.weekday() >= 5:
            if future_date.weekday() == 5:
                future_date += timedelta(days=2)
            elif future_date.weekday() == 6:
                future_date += timedelta(days=1)

        loan = Loan.objects.create(return_date=future_date, **validated_data)

        copy.is_available = False
        copy.save()

        return loan
