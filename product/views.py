from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from order.models import ShopCart, Wishlist
from .models import Comment, CommentForm


def index(request):
    return HttpResponse('Product Page')


def addcomment(request, id):
    current_user = request.user
    request.session['wish_items'] = Wishlist.objects.filter(user_id=current_user.id).count()
    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)
        else:
            print(form.errors.as_data())  # here you print errors to terminal

    return HttpResponseRedirect(url)
