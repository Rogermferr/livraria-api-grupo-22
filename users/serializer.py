from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "cpf",
            "password",
            "is_superuser",
            "full_name",
            "block_date",
            "is_blocked",
        ]
        extra_kwargs = {
            "cpf": {
                "min_length": 11,
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that cpf already exists.",
                    )
                ],
            },
            "password": {"write_only": True},
            "block_date": {"allow_null": True, "read_only": True},
            "is_blocked": {"read_only": True},
        }

    def create(self, validated_data):
        collaborator = validated_data.get("is_superuser", None)

        if collaborator:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)
