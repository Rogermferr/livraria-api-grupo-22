# Generated by Django 4.2.2 on 2023-07-03 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(default=datetime.datetime(2023, 7, 3, 18, 19, 23, 827633, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]