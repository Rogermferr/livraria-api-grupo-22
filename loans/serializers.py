from rest_framework import serializers

from copies.serializer import CopySerializer
from users.serializer import UserSerializer
from datetime import timedelta, datetime

from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    copy = CopySerializer(required=False)

    class Meta:
        model = Loan
        fields = ["id", "created_at", "updated_at", "is_finished", "user", "copy"]
        extra_kwargs = {"return_date" : {'read_only': True}}


    def create (self, validated_data):
        data_atual = datetime.now().date()
        data_futura = data_atual + timedelta(days=7)
        
        return Loan.objects.create(return_date = data_futura, **validated_data)



