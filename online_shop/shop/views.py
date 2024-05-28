from typing import Any
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from . import models
from comments .models import Comment
from django.shortcuts import redirect, render
import json


class HomeView(ListView):
    model = models.Product
    paginate_by = 4
    template_name = 'shop/home.html'


class ProductView(DetailView):
    model = models.Product
    template_name = 'shop/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product_sizes = models.ProductSize.objects.filter(product=product)
        comments = Comment.objects.filter(product=product)
        context['sizes'] = product_sizes
        context['comments'] = comments
        return context


def add_to_cart(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cart_data = json.loads(request.body)
            product_id = cart_data['product_id']
            size = cart_data['size']

            product = models.Product.objects.get(pk=product_id)
            cart, created = models.Cart.objects.get_or_create(customer=request.user)
            quantity = int(cart_data.get('quantity', 1))
            cart_item = models.CartItem.objects.filter(cart=cart, product=product, size=size).first()

            if cart_item is None:
                cart_item = models.CartItem(cart=cart, product=product, size=size, quantity=quantity)
            else:
                cart_item.quantity += quantity

            cart_item.save()
    else:
        return redirect('accounts:signup')
    
    return redirect('shop:cart')


def cart(request):
    if request.user.is_authenticated:
        cart, created = models.Cart.objects.get_or_create(customer=request.user)
        cart_items = models.CartItem.objects.filter(cart=cart)
        total = cart.get_total
        context = {
            'cart_items': cart_items,
            'total': total
        }
        return render(request, 'shop/cart.html', context)

    else:
        return redirect('accounts:signup')


def update_cart_quantity(request):
    if request.user.is_authenticated and request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')
        size = data.get('size') 

        try:
            cart_item = models.CartItem.objects.get(cart__customer=request.user, product_id=product_id, size=size)

            if action == 'add':
                cart_item.quantity += 1
            
            elif action == 'remove' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            else:
                return JsonResponse({'success': False})
            
            cart_item.save()
            return JsonResponse({'success': True})

        except models.CartItem.DoesNotExist: 
            return JsonResponse({'success': False})
        
    return JsonResponse({'success': False})


def delete_cart_item(request, pk, size):
    if request.user.is_authenticated:
        cart_item = models.CartItem.objects.get(cart__customer=request.user, product_id=pk, size=size)
        cart_item.delete()

    return redirect('shop:cart')
        

def checkout(request):
    customer = request.user
    cart = models.Cart.objects.get(customer=customer)
    cart_items = models.CartItem.objects.filter(cart=cart)
    total = cart.get_total

    if not cart_items:
        return redirect('shop:cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        order = models.Order.objects.create(customer=customer)
        for cart_item in cart_items:
            models.OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                size=cart_item.size,
                quantity = cart_item.quantity
            )
            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()


        new_address = models.ShippingAddress.objects.create(
            customer=request.user,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            order = order
        )


        cart_items.delete()

        return redirect('shop:order_success')



    return render(request, 'shop/checkout.html', {'cart_items': cart_items , 'total':total})


def order_success(request):
    return render(request, 'shop/order_success.html')


def order_view(request):
    if request.user.is_authenticated:
        customer = request.user
        orders = models.Order.objects.filter(customer=customer).order_by('-order_date')
        context = {'orders': orders}
        return render(request, 'shop/user_orders.html', context)

    else:
        return redirect('accounts:signup')


def search_results(request):
    query = request.GET.get('q')
    if query:
        products = models.Product.objects.filter(name__icontains=query)
    
    else:
        products = models.Product.objects.all()
    
    return render(request, 'shop/search_results.html', {'products': products, 'query': query})