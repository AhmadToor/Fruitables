from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from . import models
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def custom404(request, exception):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    return render(request, '404.html', {'cart_quantity' : cart_quantity})
def custom500(request):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    return render(request, '500.html', {'cart_quantity' : cart_quantity})

def home(request):
    Foods = models.Food.objects.all()
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    return render(request, 'home.html', {'Foods' : Foods, 'cart_quantity' : cart_quantity})
def cart(request):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    subtotal =   sum(item.quantity * item.product.Prize for item in Cart)
    return render(request, 'cart.html', {'Cart': Cart, 'Subtotal' : subtotal, 'cart_quantity' : cart_quantity})
def checkout(request):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    subtotal =   sum(item.quantity * item.product.Prize for item in Cart)
    return render(request, 'checkout.html', {'cart_quantity' : cart_quantity,'Cart': Cart, 'Subtotal' : subtotal })
def contact(request):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    return render(request, 'contact.html', {'cart_quantity' : cart_quantity})
def product(request,Name):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    food = models.Food.objects.get(Name=Name)
    Related_products = models.Food.objects.filter(Category= food.Category)
    return render(request, 'product.html', {'food': food, 'Related_products': Related_products, 'cart_quantity' : cart_quantity})
def shop(request):
    Cart = models.Cart.objects.all()
    cart_quantity =   len(list(item for item in Cart))
    foods = models.Food.objects.all()
    paginator = Paginator(foods, 9)  # Show 9 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop.html', {'page_obj': page_obj, 'cart_quantity' : cart_quantity})
def testimonial(request):
    return render(request, 'testimonial.html')
def account(request):
    if request.user.is_authenticated:
        Cart = models.Cart.objects.all()
        cart_quantity =   len(list(item for item in Cart))
        return render(request, 'account.html', {'cart_quantity' : cart_quantity, 'Cart': Cart, 'Name' : request.user.get_full_name})
    else:
        return redirect('loginuser')
def update_cart_quantity(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    if quantity < 1:
        return JsonResponse({'total': 0})

    try:
        product = models.Food.objects.get(Name=product_id)
        Cart = models.Cart.objects.all()
        cart_item = models.Cart.objects.get(product=product)
        cart_item.quantity = quantity
        cart_item.save()
        total = cart_item.quantity * product.Prize  # assuming product is an instance of your Product model
        subtotal =   sum(item.quantity * item.product.Prize for item in Cart)
        return JsonResponse({'total': total, 'subtotal': subtotal })
        
    except models.Cart.DoesNotExist:
        return redirect(cart)
def delete_cart_quantity(request):
    product_id = request.POST.get('product_id')
    try:
        product = models.Food.objects.get(Name=product_id)
        cart_item = models.Cart.objects.get(product=product)
        cart_item.delete()
        Cart = models.Cart.objects.all()
        subtotal =   sum(item.quantity * item.product.Prize for item in Cart)
        cart_quantity =   len(list(item for item in Cart))
        return JsonResponse({'total': subtotal, 'quantity' : cart_quantity})
        
    except models.Cart.DoesNotExist:
        return redirect(cart)
def add_cart_quantity(request):
    Cart = models.Cart.objects.all()
    product_name = request.POST.get('product')
    product = models.Food.objects.get(Name=product_name)
    quantity = request.POST.get('quantity')
    try:
        cart_item = models.Cart.objects.get(product=product, user=request.user)
        cart_item.quantity += int(quantity)
        cart_item.save()
        cart_quantity =   len(list(item for item in Cart))
        return JsonResponse({'product_Name': product.Name, 'product_src': product.src, 'quantity' : cart_quantity})
    except models.Cart.DoesNotExist:
        cart_item = models.Cart.objects.create(product=product, quantity=quantity, user=request.user)
        cart_item.save()
        cart_quantity =   len(list(item for item in Cart))
        return JsonResponse({'product_Name': product.Name, 'product_src': product.src, 'quantity' : cart_quantity})
    
    
    
def loginuser(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('account'))
            else:
                return render(request, "login.html", {'wrongpas': True})
        elif email:
            # Create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user )
            return redirect(reverse('account'))
        else:
            return render(request, "login.html", {'wrongpas': True})
    else:
        return render(request, "login.html", {'wrongpas': False})
   
def logoutuser(request):
    logout(request)
    return redirect('/')


    

   