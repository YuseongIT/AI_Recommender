from store.models import Product
from decimal import Decimal

# Clear existing products if any
Product.objects.all().delete()

# Seed products
sample_products = [
    {
        'name': 'Nissin Creamy Seafood Cup Noodles',
        'description': 'Creamy umami goodness in a cup! Try it now!',
        'price': Decimal('35.00'),
        'tags': 'food, noodles',
        'is_recommended': True
    },
    {
        'name': '7/11 Asado Siopao',
        'description': 'Classic 7/11 Asado Siopao.',
        'price': Decimal('45.00'),
        'tags': 'food',
        'is_recommended': True
    },
    {
        'name': 'Korean Sandwich',
        'description': 'Enjoy a classic Korean delicacy right now!',
        'price': Decimal('89.00'),
        'tags': 'food, healthy',
        'is_recommended': False
    }
]

for prod in sample_products:
    Product.objects.create(**prod)

print("Data cleared and re-seeded with 2 recommendations successfully!")
