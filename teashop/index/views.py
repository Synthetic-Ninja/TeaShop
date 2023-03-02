from django.shortcuts import render

from products.models import Brands, ProductCategories


def index(request):
    context = {'brands': Brands.objects.all(),
               'product_categories': ProductCategories.objects.all()}
    return render(request, 'index/index.html', context=context)
