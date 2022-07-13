from itertools import product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import render, redirect
from django.contrib import messages

from order.models import ShopCart, ShopCartForm
from product.models import *


# Create your views here.

def index(request):
    return HttpResponse('Order Page')


@login_required(login_url='/login')
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # access user session info

    checkproduct = ShopCart.objects.filter(product_id=id)  # check product in shopcart
    if checkproduct:
        control = 1  # the product is in the cart
    else:
        control = 0  # the product is not in the cart

    if request.method == "POST":
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # update shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)

    else:  # if there's no post
        if control == 1:  # update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # access user session info
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    total = 0
    for cart in shopcart:
        total += cart.product.price * cart.quantity

    context = {
        'category': category,
        'shopcart': shopcart,
        'total': total,
    }
    return render(request, 'shop/shopcart_products.html', context)