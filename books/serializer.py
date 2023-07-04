from rest_framework import serializers
from .models import Book
from copies.models import Copy
from copies.serializer import CopySerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book

        fields = ["id", "title", "author", "pages", "summary", "number_copies"]

    def create(self, validated_data):
        number_copies = validated_data.get("number_copies", 0)

        book = Book.objects.create(**validated_data)

        copies = []
        for _ in range(number_copies):
            copy_data = {}
            copy = Copy(book=book, **copy_data)
            copy.save()
            copies.append(copy)

        return book

    def get_copies(self, obj):
        copies = Copy.objects.filter(book=obj)
        serializer = CopySerializer(copies, many=True)
        return serializer.data


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book

        fields = ["id", "title", "author", "pages", "summary", "number_copies"]

        extra_kwargs = {
            "number_copies": {"read_only": True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
