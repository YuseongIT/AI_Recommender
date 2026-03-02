from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=255, blank=True, null=True)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.name