from djongo import models

class Product(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=50)

    # Hello! I added this code snippet for the challenge task.
    tags = models.CharField(max_length=255, blank=True) 

    def __str__(self):
        return self.name
