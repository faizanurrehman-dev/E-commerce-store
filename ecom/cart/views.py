from django.shortcuts import render , get_object_or_404 , redirect
from .cart import Cart
from django.http import JsonResponse
from store.models import Product
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    products = []
    subtotal = 0
    for product_id, item in cart.cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        total_price = float(item['price']) * item['quantity']
        subtotal += total_price
        products.append({
            'product': product,
            'size': item['size'],
            'quantity': item['quantity'],
            'price': item['price'],
            'total_price': total_price,
        })

    return render(request, 'cart_summary.html', {'products': products , 'subtotal' :subtotal})

def checkout(request):
    cart = Cart(request)
    products = cart.cart.items() 
    subtotal = sum(float(item['price']) * item['quantity'] for _, item in products if isinstance(item, dict))
    context = {
        'products': products,
        'subtotal': subtotal,
    }
    return render(request, 'checkout.html', context)

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        
        product_id = int(request.POST.get('product_id'))
        size = request.POST.get('size')
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product , size = size)
      
        return redirect('cart_summary') 
    return redirect('home')  

def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        
        product_id = request.POST.get('product_id')
        
        if product_id in cart.cart:
            del cart.cart[product_id]  
            
            messages.success(request, 'Product removed from your cart.')
        else:
            messages.error(request, 'Product not found in your cart.')
        
        cart.session.modified = True
        return redirect('cart_summary')  
    return redirect('home')  

def cart_update(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_change = request.POST.get('quantity')
        size = request.POST.get('size')

        product = get_object_or_404(Product, id=int(product_id))
        
        if quantity_change == '+':
            cart.add(product=product, quantity=1 , size = size)
        elif quantity_change == '-':
            
            if product_id in cart.cart and cart.cart[product_id]['quantity'] > 1:
                cart.cart[product_id]['quantity'] -= 1
                
            elif product_id in cart.cart and cart.cart[product_id]['quantity'] == 1:
                del cart.cart[product_id]  

        cart.session.modified = True
       
        return redirect('cart_summary')
    
    return redirect('home')

