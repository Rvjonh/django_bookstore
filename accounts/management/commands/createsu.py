from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username=os.getenv("ADMIN_USERNAME")).exists():
            User.objects.create_superuser(
                username=os.getenv("ADMIN_USERNAME"),
                password=os.getenv("ADMIN_PASSWORD"),
            )
        print("Superuser has been created.")
