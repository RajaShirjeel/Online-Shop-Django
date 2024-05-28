from django.shortcuts import render, redirect
from .models import Comment
from shop.models import Product
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        print('primary key ', request.user.pk)
        text = request.POST.get('comment_text')
        rating = request.POST.get('comment_rating')
        product = get_object_or_404(Product, pk=pk)
        user = User.objects.get(pk=request.user.pk)
        image = request.FILES.get('comment_image')

        print("user:", user)
        if image is not None:
            comment = Comment.objects.create(user=user, product=product, text=text, rating=rating, image=image)

        else:
            comment = Comment.objects.create(user=user, product=product, text=text, rating=rating)

    return redirect('shop:view_product', pk=pk)