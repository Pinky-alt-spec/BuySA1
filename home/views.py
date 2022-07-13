from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from home.forms import SearchForm
from product.models import *
from home.models import *


def index(request):
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

    }
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)

    context = {
        'setting': setting
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

    setting = Setting.objects.get(pk=1)
    form = ContactForm

    context = {
        'setting': setting,
        'form': form,
    }
    return render(request, 'contact.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_products.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()

            context = {
                'products': products,
                'query': query,
                'category': category,
            }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def product_details(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)

    context = {
        'category': category,
        'product': product,
        'images': images,
    }
    return render(request, 'product_details.html', context)
