from django.shortcuts import render

from .models import Products, ProductCategories, Brands


def products_list(request):

    context = {'products': Products.objects.filter(is_available=True),
               'product_categories': ProductCategories.objects.all(),
               'brands': Brands.objects.filter(),
               'title': 'Products'}

    return render(request, 'products/productlist.html', context=context)

