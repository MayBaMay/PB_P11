#!/usr/bin/env python

"""
foodSearch views
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, Http404

from .models import Category, Favorite, Product
from .query_parser import QueryParser
from .results_parser import ResultsParser
from .forms import UserCreationFormWithMail


def index(request):
    """index View"""
    return render(request, 'foodSearch/index.html')

def legals(request):
    """View rendering legals page"""
    context = {
        'title':'Mentions légales'
    }
    return render(request, 'foodSearch/legals.html', context)

def register_view(request):
    """Registration view creating a user and returning json response to ajax"""
    response_data = {}
    if request.method == 'POST':
        form = UserCreationFormWithMail(request.POST)
        if form.is_valid():
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                response_data = {'user':"email already in DB"}
            else:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                response_data = {'user':"success"}
        else:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                response_data = {'user':"diff_passwords"}
            else:
                try:
                    user = User.objects.get(username=username)
                    response_data = {'user':"already in DB"}
                except User.DoesNotExist:
                    response_data = {'user':"invalid_password"}
        return HttpResponse(JsonResponse(response_data))
    raise Http404()

def login_view(request):
    """Login view returning json response to ajax"""
    response_data = {}
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response_data = {'user':"success"}
            else:
                response_data = {'user':"error-user-none"}
        else:
            rusername = request.POST['username']
            password = request.POST['password']
            try:
                user = User.objects.get(username=username)
                if user.password != password:
                    response_data = {'user':"wrong_password"}
                else:
                    response_data = {'user':"error"}
            except User.DoesNotExist:
                response_data = {'user':"user_unknown"}
        return HttpResponse(JsonResponse(response_data))
    raise Http404()

def userpage(request):
    """View rendering userpage"""
    context={'user':request.user}
    success = False
    if request.user.is_authenticated:
        form = PasswordChangeForm(user=request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                success = True
        context['form'] = form
        context['success'] = success
        return render(request, 'foodSearch/userpage.html', context)
    return render(request, 'foodSearch/userpage.html', context)

def new_name(request):
    """View changing user name"""
    response_data = {}
    user = request.user
    if request.method == 'POST':
        new_name_user = request.POST['username']
        if User.objects.filter(username=new_name_user).exists():
            response_data = {'response':"name already in db", 'name':user.username}
        else:
            user.username = new_name_user
            user.save()
            if user.username == new_name_user:
                response_data = {'response':"success", 'name':user.username}
            else:
                response_data = {'response':"fail", 'name':user.username}
    else:
        raise Http404()
    return HttpResponse(JsonResponse(response_data))

def new_email(request):
    """View changing user email"""
    response_data = {}
    user = request.user
    if request.method == 'POST':
        new_email_user = request.POST['email']
        if User.objects.filter(email=new_email_user).exists():
            response_data = {'response':"email already in DB"}
        else:
            user.email = new_email_user
            user.save()
            if user.email == new_email_user:
                response_data = {'response':"success"}
            else:
                response_data = {'response':"fail"}
    else:
        raise Http404()
    return HttpResponse(JsonResponse(response_data))

def watchlist(request):
    """View rendering wachlist page with products saved as substitute by user"""
    current_user = request.user
    title = 'Mes aliments'
    page = request.GET.get('page')
    user_watchlist = Favorite.objects.filter(user=current_user)

    if user_watchlist.count() > 6:
        paginate = True
    else:
        paginate = False

    if paginate:
        paginator = Paginator(user_watchlist, 6)
        watchlistpage = paginator.get_page(page)
    else:
        watchlistpage = user_watchlist

    if page is None:
        page = 1

    context = {
        'page':page,
        'title':title,
        'watchlistpage':watchlistpage,
        'paginate':paginate
    }
    return render(request, 'foodSearch/watchlist.html', context)

def search(request):
    """
    View rendering search page where user confirm his search product with one in DB
    This function uses the class QueryParser from module query_parser.py
    """
    query = request.GET.get('query')
    title = query

    if query == "":
        found_products = []
    else:
        parser = QueryParser(query)
        parser.get_final_list()
        found_products = parser.product_list[0:12]

    context = {
        'title' : title,
        'found_products': found_products,
    }
    return render(request, 'foodSearch/search.html', context)

def results(request, product_id):
    """
    View rendering results page showing more relevant substitutes
    This function uses the class ResultsParser from module results_parser.py
    """
    title = Product.objects.get(id=product_id).name
    page = request.GET.get('page')
    current_user = request.user
    parser = ResultsParser(product_id, current_user)
    if page is None:
        page = 1

    context = {
        'title':title,
        'product':parser.product,
        'result': parser.paginator(page),
        'page':page,
        "paginate": parser.paginate
    }
    return render(request, 'foodSearch/results.html', context)

def detail(request, product_id):
    """View rendering detail page with product informations detail"""
    product = Product.objects.get(id=product_id)
    context = {
        'product':product
    }
    return render(request, 'foodSearch/detail.html', context)

def load_favorite(request):
    """View loading or deleting favorite row and returning a json response to ajax"""
    user = request.POST['user']
    substitute_id = request.POST['substitute']
    favorite = request.POST['favorite']
    product_id = request.POST['product']

    current_user = User.objects.get(id=user)
    if favorite == "saved":
        # delete favorite
        try:
            substitute = Product.objects.get(id=substitute_id)
            product = Product.objects.get(id=product_id)
            Favorite.objects.get(user=current_user, substitute=substitute).delete()
            favorite = "unsaved"
        except:
            print('ERROR DELETE')
    else:
        # save as favorite
        try:
            substitute = Product.objects.get(id=substitute_id)
            product = Product.objects.get(id=product_id)
            Favorite.objects.create(user=current_user,
                                    substitute=substitute,
                                    initial_search_product=product)
            favorite = "saved"
        except:
            print('ERROR SAVE')

    return HttpResponse(JsonResponse({'substitute_id': substitute_id,
                                      'product_id': product_id,
                                      'favorite': favorite}))
