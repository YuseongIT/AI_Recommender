import os
import openai
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

# Load the API key from environment variables
openai.api_key = os.getenv("OPENAI_KEY")

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
    
            try:
                prompt = f"Generate 3 short comma-separated tags for this product: {product.name}. Description: {product.description}"
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
        
                product.tags = response.choices[0].message.content.strip()
            except Exception as e:
                print(f"AI Tagging failed: {e}")
                product.tags = "General" 
            
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})