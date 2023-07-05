from rest_framework import serializers
from books.models import Book
from copies.serializer import CopySerializer
from users.models import User
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
        user = get_object_or_404(User, username=validated_data.get("user"))
        loans = Loan.objects.filter(user=user.id)
        copy_id = self.context["view"].kwargs["pk"]
        copy = get_object_or_404(Copy, id= copy_id)

        if loans:
            for loan in loans:
                if not loan.updated_at == loan.created.at:

                    if loan.updated_at > loan.return_date:
                        user.block_date = loan.updated_at + timedelta(days=3)
                        user.is_blocked = True
                    
                    if current_date > loan.return_date and not loan.is_finished:
                        user.block_date = current_date + timedelta(days=3)
                        user.is_blocked = True


                if current_date > loan.return_date and not loan.is_finished:
                    raise ValidationError({"error": "O empréstimo não pode ser criado."})
                
        if current_date > user.block_date:
            user.is_blocked = False
#
        if user.is_blocked:
            raise PermissionError(detil={"error":"Este usuario esta bloqueado."})

        if not copy.is_available:
            raise ValidationError(detail={"error": "Essa cópia não está disponível."})

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

        loan = get_object_or_404(Loan, user=validated_data.get("user"))
        copy = get_object_or_404(Copy, id=self.context["view"].kwargs["pk"])

        if future_date.weekday() >= 5:
           raise ValidationError(detail={"error": "A devolucao nao pode ser realizada aos finais de semana."})
        
        loan.is_finished = True
        copy.is_available = True
        copy.save()
        return loan