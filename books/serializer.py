from rest_framework import serializers

from _bookstore import settings
from .models import Book
from copies.models import Copy
from copies.serializer import CopySerializer
from django.core.mail import send_mail


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "pages", "summary", "number_copies", "availability"]
        extra_kwargs = {"number_copies": {"allow_null": True}}

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

        fields = ["id", "title", "author", "pages", "summary", "number_copies", "availability"]

        extra_kwargs = {
            "number_copies": {"read_only": True},
        }

    def update(self, instance, validated_data):

        check_availability = False

        for key, value in validated_data.items():
            setattr(instance, key, value)
            if key == 'availability':
                check_availability = True

        instance.save()

        if check_availability and instance.availability:

            users_followed = instance.follower.all()

            for user in users_followed:
                subject = 'Livro Disponivel'
                message = f'The book {instance.title} is available for loan'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)

        return instance
