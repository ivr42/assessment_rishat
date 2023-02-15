# Generated by Django 4.1.6 on 2023-02-15 19:24

from django.db import migrations
import os
from django.contrib.auth import get_user_model


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    def create_superuser(apps, schema_editor):
        User = get_user_model()

        credentials = {
            "username": os.environ.get("DJANGO_SUPERUSER_USERNAME"),
            "email": os.environ.get("DJANGO_SUPERUSER_EMAIL"),
            "password": os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
        }

        if (
            credentials["username"]
            and credentials["email"]
            and not User.objects.filter(email=credentials["email"]).exists()
        ):
            User.objects.create_superuser(**credentials)

    def remove_superuser(apps, schema_editor):
        User = get_user_model()

        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

        if email and User.objects.filter(email=email).exists():
            superuser = User.objects.get(email=email)
            superuser.delete()

    operations = [
        migrations.RunPython(
            create_superuser,
            remove_superuser,
        ),
    ]
