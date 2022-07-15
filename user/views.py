from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from product.models import Category
from user.forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


@login_required(login_url='/login')  # check login
def index(request):
    category = Category.objects.all()
    current_user = request.user  # access User session info

    profile = UserProfile.objects.get(user_id=current_user.id)
    # return HttpResponse(profile)
    context = {
        'category': category,
        'profile': profile,
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

            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()

    context = {
        'category': category
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
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/register')

    form = RegisterForm()
    category = Category.objects.all()

    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'login_form.html', context)


def logout_func(request):
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
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
        }
    return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def password_update(request):
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
        form = PasswordChangeForm(request.user)

        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'user_password.html', context)


def address_update(request):
    return render(request, 'user_address_update.html')
