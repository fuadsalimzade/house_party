# Generated by Django 5.0.6 on 2024-06-23 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_room_current_song_alter_room_code"),
        ("spotify", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(max_length=50, unique=True)),
                ("song", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.room"
                    ),
                ),
            ],
        ),
    ]
