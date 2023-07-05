from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(min_length=11, max_length=11)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cpf', 'password', 'is_superuser', 'full_name', 'block_date', 'is_blocked']
        extra_kwargs = {'password': {'write_only': True},
                        'block_date': {'allow_null': True, 'read_only' : True},
                        'is_blocked': {'read_only': True}}

    def create(self, validated_data):
        
        collaborator = validated_data.get('is_superuser', None)

        if collaborator:
            return User.objects.create_superuser(**validated_data)
        
        return User.objects.create_user(**validated_data)
