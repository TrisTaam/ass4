from django.core.management.base import BaseCommand
from items.models import Item
import random

class Command(BaseCommand):
    help = 'Seed items data'

    def handle(self, *args, **kwargs):
        items = [
            {"name": "Shirt", "category": "clothes"},
            {"name": "Book", "category": "book"},
            {"name": "Laptop", "category": "electronics"},
            {"name": "Shoes", "category": "footwear"},
            {"name": "Watch", "category": "accessories"},
            {"name": "Bag", "category": "accessories"},
            {"name": "Tablet", "category": "electronics"},
            {"name": "Jacket", "category": "clothes"},
            {"name": "Headphones", "category": "electronics"}
        ]

        for item in items:
            Item.objects.create(
                name=item["name"],
                category=item["category"],
                description=f"High-quality {item['name']}.",
                price=round(random.uniform(10, 500), 2),
                stock_quantity=random.randint(1, 100),
                image_url=f"/static/images/{item['name'].lower()}.jpg",  # Replace with actual images in static folder
                specific_data={}
            )

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(items)} items'))
