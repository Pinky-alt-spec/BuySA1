from itertools import product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string

from user.models import UserProfile
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import *


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
    return render(request, 'shopcart_products.html', context)


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    # profile = UserProfile.objects.get(user_id=current_user.id)
    total = 0
    for cart in schopcart:
        total += cart.product.price + cart.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # send credit card to bank and get results if returns payment info is okay to continue
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            # move shopcart items to order products items
            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for cart in schopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order id
                detail.product_id = cart.product_id
                detail.user_id = current_user.id
                detail.quantity = cart.quantity
                detail.price = cart.product.price
                detail.amount = cart.amount
                detail.save()

                # *** Reduce quantity of sold product from amount of product
                product = Product.objects.get(id=cart.product_id)
                product.amount -= cart.quantity
                product.save()
                # **********************<>*********************

            ShopCart.objects.filter(user_id=current_user.id).delete()  # clear & delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank You!")
            return render(request, 'order_complete.html', {'ordercode': ordercode, 'category': category})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderproduct')

    form = OrderForm()
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {
        'category': category,
        'schopcart': schopcart,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'order_form.html', context)
