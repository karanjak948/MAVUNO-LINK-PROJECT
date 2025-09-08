from django.core.management.base import BaseCommand
from accounts.mongo_models import MongoUser
from werkzeug.security import generate_password_hash

class Command(BaseCommand):
    help = "Create a MongoDB superuser"

    def handle(self, *args, **options):
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if MongoUser.objects(username=username).first():
            self.stdout.write(self.style.ERROR("❌ Username already exists"))
            return

        user = MongoUser(
            username=username,
            email=email,
            password=generate_password_hash(password),
            is_staff=True,
            is_superuser=True
        )
        user.save()
        self.stdout.write(self.style.SUCCESS(f"✅ Superuser '{username}' created successfully in MongoDB"))
