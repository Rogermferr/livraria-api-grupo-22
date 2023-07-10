from rest_framework import serializers
from copies.serializer import CopySerializer
from users.models import User
from users.serializer import UserSerializer
from datetime import timedelta, datetime
from .models import Loan
from rest_framework.exceptions import PermissionDenied
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
        user = get_object_or_404(User, username=validated_data.get("user"))
        loans = Loan.objects.filter(user=user.id)
        copy_id = self.context["view"].kwargs["pk"]
        copy = get_object_or_404(Copy, id=copy_id)
        book = copy.book

        if user.is_superuser:
            raise PermissionDenied({"error": "Unable to lend a book to a collaborator"})

        if not book.availability:
            raise PermissionDenied({"error": "This book is not available"})

        if loans:
            for loan in loans:
                if current_date > loan.return_date and not loan.is_finished:
                    user.block_date = current_date + timedelta(days=3)
                    user.is_blocked = True
                    user.save()
                    raise PermissionDenied({"error": "The loan cannot be created."})

        if user.block_date and current_date > user.block_date:
            user.is_blocked = False
            user.save()

        if user.is_blocked:
            raise PermissionDenied(detail={"error": "This user is blocked."})

        if not copy.is_available:
            raise PermissionDenied(detail={"error": "This copy is not available."})

        if future_date.weekday() >= 5:
            if future_date.weekday() == 5:
                future_date += timedelta(days=2)
            elif future_date.weekday() == 6:
                future_date += timedelta(days=1)

        loan = Loan.objects.create(return_date=future_date, **validated_data)

        copy.is_available = False
        copy.save()

        return loan

    def update(self, instance, validated_data):
        current_date = datetime.now().date()
        future_date = current_date + timedelta(days=7)
        user = get_object_or_404(User, username=validated_data.get("user"))
        copy = get_object_or_404(Copy, id=self.context["view"].kwargs["pk"])
        loan = Loan.objects.filter(copy=copy).first()

        if current_date > loan.return_date:
            user.block_date = loan.updated_at + timedelta(days=3)
            user.is_blocked = True
            user.save()

        if future_date.weekday() >= 5:
            raise PermissionDenied(detail={"error": "Returns cannot be made on weekends."})

        loan.is_finished = True
        copy.is_available = True
        copy.save()

        return loan
