import re
from decimal import Decimal

from django.views.generic import ListView
from django.http import QueryDict, Http404

from .models import Products, ProductCategories, Brands
from .validators import FilterValidator


class ProductsListView(ListView):
    """Класс возвращает страницу с продуктами, у которых параметр available=True"""
    paginate_by = 20
    paginate_by_list = ['All', '1', '10', '20', '30', '40']
    order_by_params = ['default', 'name', 'price']
    model = Products
    template_name = 'products/productlist.html'

    def get_queryset(self):
        return Products.objects.filter(is_available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
                'queryset_count': len(self.object_list),
                'product_categories': ProductCategories.objects.all(),
                'brands': Brands.objects.filter(),
                'title': 'Products',
                'paginate_by_list': self.paginate_by_list,
                'order_by_param': self.order_by_params,
                'filter_param': QueryDict('', mutable=True)}
        )
        return context


class ProductFilteredListView(ProductsListView):
    """Класс возвращает ProductsListView с параметрами фильтрации,
     переданными с параметрами запроса"""

    validator = FilterValidator

    def get_queryset(self):
        queryset = super().get_queryset()

        if category := self.request.GET.get('category'):
            queryset = queryset.filter(category_id=category)

        if brands := self.request.GET.getlist('brands'):
            queryset = queryset.filter(brand__id__in=brands)

        if price_filter_param := self.request.GET.get('price'):
            parsed_prices = re.sub(r'[^\d-]', '', price_filter_param).split('-')
            min_price, max_price = map(Decimal, parsed_prices)
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        if order_param := self.request.GET.get('Order_By'):
            match order_param:
                case 'price':
                    queryset = sorted(queryset, key=lambda x: x.get_discounted_price())
                case 'name':
                    queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        # Убираем дублирующийся параметр 'page'
        context['filter_param'].update(self.request.GET.copy())
        if 'page' in context['filter_param']:
            del context['filter_param']['page']
        return context

    def get(self, request, *args, **kwargs):
        if not self.validator(self.request.GET).is_valid():
            raise Http404('Invalid filter params')
        return super().get(self, request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if (product_per_page := self.request.GET.get('ProductPerPage')) is not None:
            return int(product_per_page) if product_per_page in self.paginate_by_list and product_per_page != "All" \
                                         else len(queryset)

        return len(queryset)
