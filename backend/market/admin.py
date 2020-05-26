from django.contrib import admin
from market.models import Provider, Store, Consumer, Category, Product, Order, OrderProduct, SubCategory


class ProviderAdmin(admin.ModelAdmin):
    pass


class ConsumerAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


class OrderAdmin(admin.ModelAdmin):
    pass


class OrderProductAdmin(admin.ModelAdmin):
    pass


class StoreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
