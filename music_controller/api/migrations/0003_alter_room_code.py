# Generated by Django 5.0.6 on 2024-06-15 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_room_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="code",
            field=models.CharField(default="d23f4ab6", max_length=8, unique=True),
        ),
    ]
