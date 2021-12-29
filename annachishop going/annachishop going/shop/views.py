from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .form import RegisterForm, ShopRegisterForm #AddProductsForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .formsss import *
from .serializer import *
from .models import *


def home(request):
    # if request.META['HTTP_HOST'] != "ecommerce.hem.xyz.np":
    #     return redirect("http://ecommerce.hem.xyz.np")
    products = Products.objects.filter(active=True)
    categories = Shop.objects.filter(active=True)
    context = {"products": products, "categories": categories}
    return render(request, "shop/home.html", context)


def search(request):
    q = request.GET["q"]
    products = Products.objects.filter(active=True)
    categories = Shop.objects.filter(active=True, name__icontains=q)
    context = {
        "categories": categories,
        # "title": q + " - search"
    }
    return render(request, "shop/list.html", context)


def categories(request, slug):
    cat = Shop.objects.get(slug=slug)
    products = Products.objects.filter(active=True, shop=cat)
    categories = Shop.objects.filter(active=True)
    context = {"products": products, "categories": categories, "title": cat.name + " - Categories"}
    return render(request, "shop/list.html", context)


def detail(request, slug):
    product = Products.objects.filter(active=True, slug=slug)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
        else:
            messages.error(request, "Invalid form")
    else:
        form = ReviewForm()

    categories = Shop.objects.filter(active=True)
    context = {"products": product,
               "categories": categories,
               "form": form}
    return render(request, "shop/detail.html", context)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account created succesfully for " + user)
            return redirect("shop:login")
    else:
        form = RegisterForm()
    return render(request, "shop/register.html", {"formdata": form, 'messages': messages})


def shop_signup(request):
    if request.method == 'POST':
        form = ShopRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            shop_name = form.cleaned_data['shop_name']
            shop_location = form.cleaned_data['shop_location']
            Shop_description = form.cleaned_data['Shop_description']
            mobile_number = form.cleaned_data['mobile_number']
            p = ShopRegister(name=name, shop_name=shop_name,
                             shop_location=shop_location,
                             Shop_description=Shop_description,
                             mobile_number=mobile_number)
            p.save()
            messages.success(request, "welcome" + name + "your shop has created")
            return redirect("shop:vendor")
    else:
        form = ShopRegisterForm()
    return render(request, "shop/shop_register.html", {"formdata": form, "msg": messages})


@csrf_exempt
def signin(request):
    messagess = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_customer:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("shop:home")
        elif user is not None and user.is_vendor:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("shop:vendor")
        else:
            messagess = "Invalid Username or Password"
    return render(request, "shop/login.html", {"msg": messagess})


def signout(request):
    logout(request)
    return redirect("shop:login")


def mycart(request):
    sess = request.session.get("data", {"items": []})
    products = (Products.objects.filter(active=True, slug__in=sess["items"]))
    # products = Products.objects.filter(active=True, slug__in=sess["items"])
    print(products)
    categories = Shop.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": "My Cart"}
    return render(request, "shop/cartproduct.html", context)


def checkout(request):
    request.session.pop('data', None)
    return redirect("/")


@api_view(['GET'])
def api_products(request):
    query = request.GET.get("q", "")
    products = Products.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def vendor(request):
    user = request.user
    print(user)
    data = ShopRegister.objects.filter(name=user)
    return render(request, 'shop/vendor.html', {'data': data})


def add_product(request):
    if request.method == 'POST':
        form = AddProductsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            shop_name = form.cleaned_data['shop_name']
            shop_location = form.cleaned_data['shop_location']
            Shop_description = form.cleaned_data['Shop_description']
            mobile_number = form.cleaned_data['mobile_number']
            p = ShopRegister(name=name, shop_name=shop_name,
                             shop_location=shop_location,
                             Shop_description=Shop_description,
                             mobile_number=mobile_number)
            p.save()
            messages.success(request, "welcome" + name + "your shop has created")
            return redirect("shop:vendor")
    else:
        form = ShopRegisterForm()
    return render(request, 'add_products.html')


def cart(request, slug):
    if request.user.is_authenticated:
        user = request.user
        order, created = Orders.objects.get_or_create(customer=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'product': order, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cartproduct.html', context)


def carts(request, slug):
    """
        data = {"items" : ["slug1", "slug2"],
                "price" : 12342,
                "count" : 5
                }
        request.session["data"] = data
        """
    product = Products.objects.get(slug=slug)
    user = request.user
    order, created = Orders.objects.get_or_create(customer=user, product=product, complete=False)
    inital = {"items": [], "price": 0.0, "count": 0}
    session = request.session.get("data", inital)
    if slug in session["items"]:
        messages.error(request, "Already added to cart")
    else:
        session["items"].append(slug)
        session["price"] += float(product.price)
        session["count"] += 1
        request.session["data"] = session
        messages.success(request, "Added successfully")
    return redirect("shop:detail", slug)


def profile(request):
    user = request.user
    profile_details = UserProfile.objects.filter(name=user)
    return render(request, 'shop/profile.html', {'datas': profile_details})
