from rest_framework import serializers
from .models import Copy
from books.models import Book


class CopySerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = Copy

        fields = ["id", "book_id", "book_title", "is_available"]

        extra_kwargs = {
            "book_id": {"read_only": True},
        }

        def create(self, validated_data):
            return Copy.objects.create(**validated_data)

    def get_book_title(self, obj):
        return obj.book.title
