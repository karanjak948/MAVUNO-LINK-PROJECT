from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Seed database with demo products"

    def handle(self, *args, **kwargs):
        products = [
            {
                "name": "Hybrid Maize Seeds",
                "category": "Seeds",
                "description": "High-yield hybrid maize seeds resistant to drought and pests.",
                "price": 2500,
                "stock": 120,
                "seller": "AgriSeeds Ltd",
                "rating": 4.0,
                "reviews_count": 45,
                "image": "products/maize_seeds.jpg"
            },
            {
                "name": "Organic Fertilizer (50kg)",
                "category": "Fertilizers",
                "description": "Eco-friendly organic fertilizer that improves soil health.",
                "price": 3800,
                "stock": 60,
                "seller": "GreenGrow Supplies",
                "rating": 5.0,
                "reviews_count": 68,
                "image": "products/fertilizer.jpg"
            },
            {
                "name": "Knapsack Sprayer (16L)",
                "category": "Equipment",
                "description": "Durable 16-liter knapsack sprayer for pesticides and herbicides.",
                "price": 6200,
                "stock": 35,
                "seller": "FarmTools Kenya",
                "rating": 4.0,
                "reviews_count": 29,
                "image": "products/sprayer.jpg"
            },
            {
                "name": "Tomato Seeds (Packet)",
                "category": "Seeds",
                "description": "Disease-resistant tomato seeds with high fruit yield.",
                "price": 800,
                "stock": 200,
                "seller": "FreshGrow Kenya",
                "rating": 4.5,
                "reviews_count": 52,
                "image": "products/tomato_seeds.jpg"
            },
            {
                "name": "Chicken Feeds (50kg)",
                "category": "Feeds",
                "description": "Nutritious layer feeds to boost egg production.",
                "price": 3200,
                "stock": 75,
                "seller": "PoultryCare Ltd",
                "rating": 4.8,
                "reviews_count": 61,
                "image": "products/chicken_feeds.jpg"
            },
            {
                "name": "Pesticide Spray (1L)",
                "category": "Chemicals",
                "description": "Effective pest control solution for vegetables and cereals.",
                "price": 1500,
                "stock": 90,
                "seller": "AgroChem Distributors",
                "rating": 4.3,
                "reviews_count": 38,
                "image": "products/pesticide.jpg"
            },
            {
                "name": "Irrigation Pipe (30m)",
                "category": "Equipment",
                "description": "Durable PVC irrigation pipe suitable for small farms.",
                "price": 5400,
                "stock": 25,
                "seller": "WaterTech Africa",
                "rating": 4.6,
                "reviews_count": 27,
                "image": "products/irrigation_pipe.jpg"
            },
            {
                "name": "Hand Hoe",
                "category": "Tools",
                "description": "Strong steel hoe with wooden handle, ideal for tillage.",
                "price": 700,
                "stock": 150,
                "seller": "FarmTools Kenya",
                "rating": 4.2,
                "reviews_count": 40,
                "image": "products/hand_hoe.jpg"
            },
            {
                "name": "Greenhouse Polythene (200 microns)",
                "category": "Equipment",
                "description": "UV-treated greenhouse polythene sheet for crop protection.",
                "price": 14500,
                "stock": 10,
                "seller": "AgriPlast Ltd",
                "rating": 4.7,
                "reviews_count": 18,
                "image": "products/greenhouse_polythene.jpg"
            },
        ]

        for item in products:
            obj, created = Product.objects.get_or_create(
                name=item["name"],
                defaults=item
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"{obj.name} already exists"))
