import os
import cv2
import numpy as np
from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile
from search.models import Category, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds the database with elite tech categories and high-quality products'

    def handle(self, *args, **options):
        # 1. Define Categories
        categories_data = ['Smartphones', 'Laptops', 'Audio', 'Gaming', 'Accessories']
        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = cat
            if created:
                self.stdout.write(f"Created category: {cat_name}")

        # 2. Define Products
        # Note: We assume the images are in the artifacts folder and we copy them to media later or directly use them
        products_data = [
            {
                'name': 'MacBook Pro M3',
                'category': 'Laptops',
                'price': 45000,
                'size': '14 inch',
                'asset': 'macbook_pro_m3_1770407908551.png'
            },
            {
                'name': 'iPhone 15 Pro Max',
                'category': 'Smartphones',
                'price': 22000,
                'size': '256GB',
                'asset': 'iphone_15_pro_max_blue_1770407923012.png'
            },
            {
                'name': 'Sony WH-1000XM5',
                'category': 'Audio',
                'price': 7500,
                'size': 'Black',
                'asset': 'sony_wh_1000xm5_black_1770407943027.png'
            },
            {
                'name': 'Elite RTX 4090 PC',
                'category': 'Gaming',
                'price': 65000,
                'size': 'Ultimate',
                'asset': 'rtx_4090_gaming_pc_1770407967238.png'
            },
            {
                'name': 'Apple Watch Ultra 2',
                'category': 'Accessories',
                'price': 14000,
                'size': 'Titanium',
                'asset': 'apple_watch_ultra_2_black_1770408038520.png'
            }
        ]

        artifact_dir = '/home/kkk/.gemini/antigravity/brain/b1557196-299d-4780-a5c0-a83d5c0b6013'

        for p_info in products_data:
            asset_path = os.path.join(artifact_dir, p_info['asset'])
            if not os.path.exists(asset_path):
                self.stdout.write(self.style.WARNING(f"Asset not found for {p_info['name']}: {asset_path}"))
                continue

            # Create product
            product, created = Product.objects.get_or_create(
                name=p_info['name'],
                category=categories[p_info['category']],
                defaults={
                    'price': p_info['price'],
                    'size': p_info['size']
                }
            )

            if created:
                # Open and save image
                with open(asset_path, 'rb') as f:
                    product.image.save(p_info['asset'], DjangoFile(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"Successfully seeded product: {p_info['name']}"))
            else:
                self.stdout.write(f"Product already exists: {p_info['name']}")

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
