from rest_framework import serializers
from .models import Copy
from books.models import Book


class CopySerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = Copy

        fields = ["id", "book_title"]

    def get_book_title(self, obj: Book):
        return obj.title
