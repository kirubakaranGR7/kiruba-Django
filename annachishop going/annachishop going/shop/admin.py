from django.contrib import admin

# Register your models here.

from .models import Products, Shop, Review, User, Orders, OrderItem, UserProfile, ShopRegister

# admin.site.register(Products)
# admin.site.register(Shop)
admin.site.register(Review)
admin.site.register(User)


class ShopInline(admin.TabularInline):
    model = Products


class ShopAdmin(admin.ModelAdmin):
    inlines = [
        ShopInline,
    ]

    class Meta:
        model = Shop


admin.site.register(Shop, ShopAdmin)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(ShopRegister)
