# Generated by Django 5.0.6 on 2024-06-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Spotify",
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
                ("access_token", models.CharField(max_length=150)),
                ("refresh_token", models.CharField(max_length=150)),
                ("expires_in", models.DateTimeField()),
                ("token_type", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
