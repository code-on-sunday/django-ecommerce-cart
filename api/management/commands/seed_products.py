from django.core.management.base import BaseCommand
from api.models import Product, seed_products

class Command(BaseCommand):
    help = 'Seeds the database with sample products'

    def handle(self, *args, **options):
        seed_products()
        self.stdout.write(self.style.SUCCESS('Successfully seeded products'))