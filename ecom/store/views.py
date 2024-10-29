from django.shortcuts import render, redirect , HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def product(request,pk):
    product = Product.objects.get(id =pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_list(request):
    gender = request.GET.get('gender')
    print(f"Selected gender: {gender}")  
    if gender in ['men', 'women']:
        products = Product.objects.filter(gender=gender)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'product_list.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
           
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
  
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')  

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('register')
        
        my_user = User.objects.create_user(username=username, email=email, password=pass1)
        my_user.save()
       
        return redirect('login') 

    return render(request, 'register.html')