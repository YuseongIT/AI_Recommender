from store.models import Product
from decimal import Decimal

print("--- Product List Debug ---")
for p in Product.objects.all():
    print(f"ID: {p.id}")
    print(f"Name: {p.name}")
    print(f"Price: {p.price} (Type: {type(p.price)})")
    print(f"Is Recommended: {p.is_recommended}")
    print("-" * 20)
