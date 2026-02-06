import os
import cv2
import numpy as np
from django.core.management.base import BaseCommand
from search.models import Product
from search.views import extract_features

class Command(BaseCommand):
    help = 'Indexes products by extracting and storing image features'

    def handle(self, *args, **options):
        products = Product.objects.filter(features__isnull=True)
        count = products.count()
        self.stdout.write(f"Found {count} products to index.")

        for i, product in enumerate(products):
            if not product.image:
                continue
            
            self.stdout.write(f"[{i+1}/{count}] Indexing {product.name}...")
            
            try:
                img = cv2.imread(product.image.path)
                if img is not None:
                    features = extract_features(img)
                    product.features = features.tobytes()
                    product.save(update_fields=['features'])
                else:
                    self.stderr.write(f"Could not read image for {product.name} at {product.image.path}")
            except Exception as e:
                self.stderr.write(f"Error indexing {product.name}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Successfully indexed products."))
