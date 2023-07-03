from rest_framework import serializers

# from copies.serializers import CopySerializer
# from users.serializers import UsersSerializer

from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    # user = UsersSerializer(required=False)
    # copy = CopySerializer(required=False)

    class Meta:
        model = Loan
        fields = ["id", "created_at", "updated_at", "return_date", "status", "user"]
        read_only_fields = ["user_id", "copy_id"]
