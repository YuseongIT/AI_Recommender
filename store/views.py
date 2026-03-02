import os
import openai
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def product_list(request):
    products = Product.objects.all()
    recommendations = Product.objects.filter(is_recommended=True)
    return render(request, 'store/product_list.html', {
        'products': products,
        'recommendations': recommendations
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            
            # AI Logic
            try:
                # Generate Tags
                tag_prompt = f"Generate 3 short comma-separated tags for: {product.name}"
                tag_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": tag_prompt}]
                )
                product.tags = tag_response.choices[0].message.content.strip()

                # AI Recommendation
                rec_prompt = f"Is '{product.name}' a premium item? Answer 'Yes' or 'No'."
                rec_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": rec_prompt}]
                )
                if "Yes" in rec_response.choices[0].message.content:
                    product.is_recommended = True
                
            except Exception as e:
                print(f"AI Error: {e}")
                product.tags = "General"
            
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})