from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import datetime

from users.models import User
from products.models import Product, Purchases, Report


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/admin')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    print('user.is_superuser')
                    login(request, user)
                    return HttpResponseRedirect('/admin')
                else:
                    messages.error(request, "You are authenticated, but are not authorized to access this page. Would "
                                            "you "
                                            "like to login to a different account?")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request=request, template_name="auth/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/admin/login')


def user_list_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.all().exclude(is_superuser=True)
        return render(request, 'users_list.html', context={"users": users})

    return render(request, 'auth/login.html')


def user_detail_view(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            user = User.objects.get(id=pk)
            return JsonResponse(
                data={
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "name": user.name,
                    "create": user.date_joined,
                    "last": user.last_login,
                    "mobile": user.phone,
                    "active": user.is_active,
                    "address": user.address,
                    "over": user.overview,
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(data=None, status=500)
    else:
        return JsonResponse(data=None, status=401)


def user_edit_view(request, pk):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(id=pk)
            return JsonResponse(
                data={
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "name": user.name,
                    "create": user.date_joined,
                    "last": user.last_login,
                    "mobile": user.phone,
                    "active": user.is_active,
                    "address": user.address,
                    "over": user.overview,
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(data=None, status=500)
    else:
        return JsonResponse(data=None, status=401)


def user_add_view(request):
    if request.POST.get('book_id'):
        user = User.objects.get(id=request.POST.get('book_id'))
        if not request.POST.get('mobile'):
            user.phone = None
        else:
            user.phone = request.POST.get('mobile')
        if request.POST.get('address'):
            user.address = request.POST.get('address')
        else:
            user.address = None
        if request.POST.get('over'):
            user.overview = request.POST.get('over')
        else:
            user.overview = None
        if request.POST.get('active'):
            user.is_active = request.POST.get('active')
        else:
            user.is_active = 'True'
        user.save()
        return HttpResponseRedirect('/admin')

    else:
        if request.POST.get('name') and request.POST.get('email'):
            user = User()
            user.email = request.POST.get('email')
            if request.POST.get('username'):
                user.username = request.POST.get('username')
            else:
                user.username = 'NoName'
            user.name = request.POST.get('name')
            if not request.POST.get('mobile'):
                user.phone = None
            else:
                user.phone = request.POST.get('mobile')
            user.is_active = 'True'
            if request.POST.get('address'):
                user.address = request.POST.get('address')
            else:
                user.address = None
            if request.POST.get('over'):
                user.overview = request.POST.get('over')
            else:
                user.overview = None
            if request.POST.get('create'):
                user.date_joined = request.POST.get('create')
            else:
                user.date_joined = datetime.datetime.now()
            if request.POST.get('last'):
                user.last_login = request.POST.get('last')
            else:
                user.last_login = None
            user.save()
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/admin')
    return HttpResponseRedirect('/admin')


def user_delete_view(request, pk):
    try:
        User.objects.get(id=pk).delete()
        return HttpResponseRedirect('/admin')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/admin')


def product_list_view(request):
    if request.user.is_authenticated:
        products = Product.objects.all()

        all_products = []
        for product in products:
            all_products.append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "currency": product.currency,
                "description": product.description,
                "category": product.category.name,
                "user": product.user,
                "created_at": product.created_at,
                "active": product.available,
            })

        return render(request, 'products_list.html', context={"products": all_products})

    return render(request, 'auth/login.html')


def product_detail_view(request, pk):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id=pk)
            return JsonResponse(
                data={
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                    "currency": product.currency,
                    "description": product.description,
                    "category": product.category.name,
                    "user": product.user.email,
                    "updated": product.updated_at,
                    "created": product.created_at,
                    "active": product.available,
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(data=None, status=500)
    else:
        return JsonResponse(data=None, status=401)


def product_edit_view(request, pk):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id=pk)
            return JsonResponse(
                data={
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                    "currency": product.currency,
                    "description": product.description,
                    "category": product.category.name,
                    "user": product.user.email,
                    "updated": product.updated_at,
                    "created": product.created_at,
                    "active": product.available,
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(data=None, status=500)
    else:
        return JsonResponse(data=None, status=401)


def product_add_view(request):
    if request.POST.get('book_id'):
        product = Product.objects.get(id=request.POST.get('book_id'))
        if request.POST.get('username'):
            product.price = request.POST.get('username')
        else:
            product.price = '0'
        if request.POST.get('email'):
            product.title = request.POST.get('email')
        else:
            product.title = 'No Title'
        if not request.POST.get('name'):
            product.currency = '$'
        else:
            product.currency = request.POST.get('name')
        if request.POST.get('active'):
            product.available = request.POST.get('active')
        else:
            product.available = 'True'
        if request.POST.get('address'):
            product.description = request.POST.get('address')
        else:
            product.description = 'No Description'
        product.user.email = request.POST.get('over')
        if request.POST.get('create'):
            product.created_at = request.POST.get('create')
        else:
            product.created_at = datetime.datetime.now()
        if request.POST.get('last'):
            product.updated_at = request.POST.get('last')
        else:
            product.updated_at = datetime.datetime.now()
        product.save()
        return HttpResponseRedirect('/admin/products-list')

    else:
        product = Product()
        if request.POST.get('username'):
            product.price = request.POST.get('username')
        else:
            product.price = '0'
        if request.POST.get('email'):
            product.title = request.POST.get('email')
        else:
            product.title = 'No Title'
        if not request.POST.get('name'):
            product.currency = '$'
        else:
            product.currency = request.POST.get('name')
        product.available = 'True'
        if request.POST.get('address'):
            product.description = request.POST.get('address')
        else:
            product.description = 'No Description'
        product.user.email = request.POST.get('over')
        if request.POST.get('create'):
            product.created_at = request.POST.get('create')
        else:
            product.created_at = datetime.datetime.now()
        if request.POST.get('last'):
            product.updated_at = request.POST.get('last')
        else:
            product.updated_at = datetime.datetime.now()
        product.save()
        return HttpResponseRedirect('/admin/products-list')
    return HttpResponseRedirect('/admin/products-list')


def product_delete_view(request, pk):
    try:
        Product.objects.get(id=pk).delete()
        return HttpResponseRedirect('/admin/products-list')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/admin/products-list')


def transaction_list_view(request):
    if request.user.is_authenticated:
        products = Purchases.objects.all()

        all_products = []
        for product in products:
            all_products.append({
                "id": product.id,
                "title": product.product.title,
                "price": product.product.price,
                "currency": product.product.currency,
                "description": product.product.category.name,
                "category": product.product.user.email,
                "user": product.user.email,
                "created_at": product.created_at,
                "active": product.state,
            })

        return render(request, 'transactions_list.html', context={"products": all_products})

    return render(request, 'auth/login.html')


def transaction_detail_view(request, pk):
    if request.user.is_authenticated:
        try:
            product = Purchases.objects.get(id=pk)
            print(product.id)
            return JsonResponse(
                data={
                    "id": product.id,
                    "title": product.product.title,
                    "price": product.product.price,
                    "currency": product.product.currency,
                    "description": product.product.category.name,
                    "category": product.product.user.email,
                    "user": product.user.email,
                    "created": product.created_at,
                    "updated": product.updated_at,
                    "active": product.state,
                }
            )
            print(product.updated_at)
        except ObjectDoesNotExist:
            return JsonResponse(data=None, status=500)
    else:
        return JsonResponse(data=None, status=401)


def transaction_edit_view(request, pk):
    if request.user.is_authenticated:
        try:
            product = Purchases.objects.get(id=pk)
            return JsonResponse(
                data={
                    "id": product.id,
                    "title": product.product.title,
                    "price": product.product.price,
                    "currency": product.product.currency,
                    "description": product.product.category.name,
                    "category": product.product.user.email,
                    "user": product.user.email,
                    "created": product.created_at,
                    "updated": product.updated_at,
                    "active": product.state,
                }
            )
        except ObjectDoesNotExist:
            return JsonResponse(data=None, status=500)
    else:
        return JsonResponse(data=None, status=401)


def transaction_add_view(request):
    if request.POST.get('book_id'):
        product = Purchases.objects.get(id=request.POST.get('book_id'))
        if request.POST.get('active'):
            product.state = request.POST.get('active')
        else:
            product.available = '2'
        product.save()
        return HttpResponseRedirect('/admin/transactions-list')

    return HttpResponseRedirect('/admin/transactions-list')


def transaction_delete_view(request, pk):
    try:
        Purchases.objects.get(id=pk).delete()
        return HttpResponseRedirect('/admin/transactions-list')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/admin/transactions-list')


def report_list_view(request):
    if request.user.is_authenticated:
        reports = Report.objects.all()

        all_reports = []
        for report in reports:
            all_reports.append({
                "id": report.id,
                "reporter": report.reporter,
                "product": report.product.title,
                "product_owner": report.user,
                "created_at": report.created_at,
            })

        return render(request, 'reports_list.html', context={"reports": all_reports})

    return render(request, 'auth/login.html')
