
from django.urls import path
from shop import views

app_name = "shop"

urlpatterns = [
    path('', views.signup, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.signin, name="login"),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name="signout"),
    path('vendor/', views.vendor, name='vendor'),
    path('vendorshop/', views.shop_signup, name="shop_signup"),
    path('add_products/', views.add_product, name='add_products'),
    path('search/', views.search, name="search"),
    path('<slug>/cart/', views.carts, name="cart"),
    path('mycart/', views.mycart, name="mycart"),
    path('checkout/', views.checkout, name="checkout"),
    path('<slug>/', views.detail, name="detail"),
    path('categories/<slug>/', views.categories, name="product"),
    path('api/products/', views.api_products, name="api_products"),
]