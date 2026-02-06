from django.db import models
import numpy as np

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Allow nulls
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, null=True, blank=True)  # Example field
    features = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new_image = False
        if self.pk:
            old_product = Product.objects.get(pk=self.pk)
            if old_product.image != self.image:
                is_new_image = True
        else:
            is_new_image = True

        super().save(*args, **kwargs)

        if is_new_image and self.image:
            from .views import extract_features
            import cv2
            img = cv2.imread(self.image.path)
            if img is not None:
                features = extract_features(img)
                self.features = features.tobytes()
                # Update without calling save recursive
                Product.objects.filter(pk=self.pk).update(features=self.features)
