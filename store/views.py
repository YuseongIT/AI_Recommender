def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
    
            try:

                tag_prompt = f"Generate 3 short comma-separated tags for: {product.name}"
                tag_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": tag_prompt}]
                )
                product.tags = tag_response.choices[0].message.content.strip()

  
                rec_prompt = f"Is the product '{product.name}' highly rated or essential? Answer only 'Yes' or 'No'."
                rec_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": rec_prompt}]
                )
                
    
                if "Yes" in rec_response.choices[0].message.content:
                    product.is_recommended = True
                
            except Exception as e:
                print(f"AI Logic failed: {e}")
                product.tags = "General"
            
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})