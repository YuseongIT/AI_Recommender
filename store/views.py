import os
import openai
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def get_mongo_collection():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client['ecommerce_db']
    return db['store_product']

def product_list(request):
    collection = get_mongo_collection()
    
    # Get all products
    products = list(collection.find({}))
    
    # Get recommended products
    recommendations = list(collection.find({"is_recommended": True}))
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'recommendations': recommendations
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Enhanced AI Logic
            try:
                # Generate more specific tags based on product details
                tag_prompt = f"""Generate 3-5 specific, relevant tags for this product:
Name: {product.name}
Description: {product.description}
Price: ${product.price}

Return only comma-separated tags like: electronics,premium,smart-home,wireless"""
                
                tag_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a product categorization expert. Generate concise, relevant tags for products."},
                        {"role": "user", "content": tag_prompt}
                    ],
                    max_tokens=50,
                    temperature=0.7
                )
                product.tags = tag_response.choices[0].message.content.strip()

                # Enhanced AI Recommendation Logic
                rec_prompt = f"""Analyze this product and determine if it should be recommended:
Name: {product.name}
Description: {product.description}
Price: ${product.price}

Consider these factors:
- Is it a premium/high-quality item?
- Is the price above $50 (indicating quality)?
- Does it have special features?
- Would you personally recommend this to a friend?

Answer with only 'Yes' or 'No'."""
                
                rec_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a product recommendation expert. Evaluate products objectively."},
                        {"role": "user", "content": rec_prompt}
                    ],
                    max_tokens=10,
                    temperature=0.3
                )
                
                response_text = rec_response.choices[0].message.content.strip().lower()
                product.is_recommended = "yes" in response_text
                
            except Exception as e:
                print(f"AI Error: {e}")
                # Fallback logic based on price
                product.tags = "general"
                product.is_recommended = product.price > 50
            
            # Save using Django ORM for consistency
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})