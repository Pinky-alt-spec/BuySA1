from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from buysa import settings
from home.models import FAQ, Setting

from order.models import Order, OrderProduct, ShopCart
from product.models import Category, Comment
from user.forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


@login_required(login_url='/login')  # check login
def user_profile(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user  # access User session info
    profile = UserProfile.objects.get(user_id=current_user.id)
    orders = Order.objects.filter(user_id=current_user.id).order_by('-id')[:3]
    # return HttpResponse(profile)

    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'profile': profile,
        'orders': orders,
        'shopcart': shopcart,
        'setting': setting,
    }
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url

            messages.success(request, f"Login Success !! You are logged in as {username}")
            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {
        'category': category,
        'setting': setting,
    }
    return render(request, 'login_form.html', context)


def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image="images/users/user.png"
            data.save()

            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/register')

    form = RegisterForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {
        'setting': setting,
        'category': category,
        'form': form,
    }
    return render(request, 'register_form.html', context)


def logout_func(request):
    setting = Setting.objects.get(pk=1)
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)

        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'shopcart': shopcart,
            'setting': setting,
        }
    return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def password_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Incorrect Username or Password.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')

    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = PasswordChangeForm(request.user)

        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)

        context = {
            'form': form,
            'category': category,
            'shopcart': shopcart,
            'setting': setting,
        }
        return render(request, 'user_password.html', context)


@login_required(login_url='/login')
def user_orders(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'orders': orders,
        'shopcart': shopcart,
        'setting': setting,
    }

    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')
def user_orderdetail(request, id):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'shopcart': shopcart,
        'setting': setting,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')
def user_order_product(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'order_product': order_product,
        'shopcart': shopcart,
        'setting': setting,
    }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/login')
def user_order_product_detail(request, id, oid):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'shopcart': shopcart,
        'setting': setting,
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'comments': comments,
        'shopcart': shopcart,
        'setting': setting,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_delete_comment(request, id):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'faq': faq,
        'shopcart': shopcart,
        'setting': setting,
    }
    return render(request, 'faq.html', context)
