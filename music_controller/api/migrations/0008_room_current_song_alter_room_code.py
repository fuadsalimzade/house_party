# Generated by Django 5.0.6 on 2024-06-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_alter_room_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="current_song",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="room",
            name="code",
            field=models.CharField(default="C37741BC", max_length=8, unique=True),
        ),
    ]
