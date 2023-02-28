from django.contrib import admin

from .models import Products,ProductCategories,Brands


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'quantity')
    fields = ('is_available', 'name', 'description',
              'price', 'discount', 'quantity',
              'image', 'category', 'brand')


@admin.register(ProductCategories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description')


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description')



