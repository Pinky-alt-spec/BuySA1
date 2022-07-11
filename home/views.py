from django.shortcuts import render


def index(request):
    # setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    # product_featured = Product.objects.all().order_by('?')[:16]
    # product_best_seller = Product.objects.all().order_by('id')[:6]
    # product_popular = Product.objects.all().order_by('id')[:6]
    # product_new_arrival = Product.objects.all().order_by('-id')[:16]
    # product_top_related = Product.objects.all().order_by('?')[:9]
    # bottom_product_top_related = Product.objects.all().order_by('?')[:3]
    # product_featured_item = Product.objects.all().order_by('-id')[:1]
    # special_offer = Product.objects.all().order_by('id')[:3]
    # best_bottom = Product.objects.all().order_by('?')[:3]
    #
    # page = "home"
    #
    # context = {
    #     'page': page,
    #     'setting': setting,
    #     'category': category,
    #     'product_featured': product_featured,
    #     'product_best_seller': product_best_seller,
    #     'product_popular': product_popular,
    #     'product_new_arrival': product_new_arrival,
    #     'product_top_related': product_top_related,
    #     'bottom_product_top_related': bottom_product_top_related,
    #     'product_featured_item': product_featured_item,
    #     'special_offer': special_offer,
    #     'best_bottom': best_bottom,
    # }
    return render(request, 'index.html')
