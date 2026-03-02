import os
import openai
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def product_list(request):
    # Fetch all products and filter in Python to avoid djongo boolean filter bug
    all_products = list(Product.objects.all())
    
    # Convert Decimal128 to standard Decimal for template rendering
    for p in all_products:
        if hasattr(p.price, 'to_decimal'):
            p.price = p.price.to_decimal()
    
    # Filter for recommendations in memory and limit to exactly 2
    recommendations = [p for p in all_products if p.is_recommended][:2]
    
    return render(request, 'store/product_list.html', {
        'products': all_products,
        'recommendations': recommendations
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            
            # v0.28.1 OpenAI Logic
            try:
                # Generate 3 comma-separated tags
                tag_prompt = f"Product Name: {product.name}\nDescription: {product.description}\n\nGenerate exactly 3 comma-separated tags for this product."
                
                tag_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates product tags."},
                        {"role": "user", "content": tag_prompt}
                    ],
                    max_tokens=30,
                    temperature=0.7
                )
                product.tags = tag_response.choices[0].message.content.strip()

                # Decide if product should be recommended
                rec_prompt = f"Product Name: {product.name}\nDescription: {product.description}\n\nShould this product be recommended? Answer 'Yes' or 'No' only."
                
                rec_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You decide if a product is worthy of recommendation."},
                        {"role": "user", "content": rec_prompt}
                    ],
                    max_tokens=5,
                    temperature=0.3
                )
                
                response_text = rec_response.choices[0].message.content.strip().lower()
                product.is_recommended = "yes" in response_text
                
            except Exception as e:
                print(f"AI Error: {e}")
                # Fallback
                product.tags = "general,product,ecommerce"
                product.is_recommended = False
            
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})
