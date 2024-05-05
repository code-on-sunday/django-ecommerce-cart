from django.core.management.base import BaseCommand
from api.models import User, seed_users

class Command(BaseCommand):
    help = 'Seeds the database with sample users'

    def handle(self, *args, **options):
        seed_users()
        self.stdout.write(self.style.SUCCESS('Successfully seeded users'))