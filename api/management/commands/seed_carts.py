from django.core.management.base import BaseCommand
from api.models import seed_users, seed_products, seed_carts

class Command(BaseCommand):
    help = 'Seeds the database with sample carts and cart items'

    def handle(self, *args, **options):
        seed_carts()
        self.stdout.write(self.style.SUCCESS('Successfully seeded carts and cart items'))