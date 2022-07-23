import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from home.forms import SearchForm
from order.models import ShopCart
from product.models import *
from home.models import *
from user.models import UserProfile


def index(request):
    current_user = request.user

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url

            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product_featured = Product.objects.all().order_by('?')[:16]
    product_best_seller = Product.objects.all().order_by('id')[:6]
    singleproduct = Product.objects.all().order_by('id')[:1]
    product_popular = Product.objects.all().order_by('id')[:6]
    product_new_arrival = Product.objects.all().order_by('-id')[:16]
    product_top_related = Product.objects.all().order_by('?')[:3]
    special_offer = Product.objects.all().order_by('?')[:3]
    best_bottom = Product.objects.all().order_by('?')[:3]
    product_featured_item = Product.objects.all().order_by('-id')[:1]

    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    # Site Cart Dropdown
    total = 0
    for cart in shopcart:
        total += cart.product.price * cart.quantity

    page = "home"

    context = {
        'page': page,
        'setting': setting,
        'category': category,
        'product_featured': product_featured,
        'product_best_seller': product_best_seller,
        'singleproduct': singleproduct,
        'product_popular': product_popular,
        'product_new_arrival': product_new_arrival,
        'product_top_related': product_top_related,
        'special_offer': special_offer,
        'best_bottom': best_bottom,
        'product_featured_item': product_featured_item,
        'shopcart': shopcart,
        'total': total,

    }
    return render(request, 'index.html', context)


def about(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'setting': setting,
        'shopcart': shopcart,
        'category': category,
    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.subject = form.cleaned_data['subject']
            data.email = form.cleaned_data['email']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message has been sent, we will be in touch with you shortly")
            return HttpResponseRedirect('/contact')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactForm

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'setting': setting,
        'form': form,
        'shopcart': shopcart,
        'category': category,
    }
    return render(request, 'contact.html', context)


def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    catdata = Category.objects.get(pk=id)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'setting': setting,
        'products': products,
        'shopcart': shopcart,
        'catdata': catdata,
    }
    return render(request, 'category_products.html', context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            setting = Setting.objects.get(pk=1)
            current_user = request.user
            shopcart = ShopCart.objects.filter(user_id=current_user.id)

            context = {
                'products': products,
                'setting': setting,
                'query': query,
                'category': category,
                'shopcart': shopcart,
            }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for prod in products:
            product_json = {}
            product_json = prod.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_details(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)

    # query = request.GET.get('q')
    comments = Comment.objects.filter(product_id=id, status="True")

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'setting': setting,
        'product': product,
        'images': images,
        'comments': comments,
        'shopcart': shopcart,
    }

    return render(request, 'product_details.html', context)
