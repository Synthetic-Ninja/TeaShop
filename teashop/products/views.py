import re
from decimal import Decimal

from django.views.generic import ListView

from .models import Products, ProductCategories, Brands


class ProductsListView(ListView):
    """Class returns productlist template with all available products"""

    paginate_by = 20
    model = Products
    template_name = 'products/productlist.html'

    def get_queryset(self):
        return Products.objects.filter(is_available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
                'product_categories': ProductCategories.objects.all(),
                'brands': Brands.objects.filter(),
                'title': 'Products'}
        )
        pass
        return context


class ProductFilteredListView(ProductsListView):
    """Class returns productlist template with filtered products"""

    def get_queryset(self):
        queryset = super().get_queryset()

        if brands := self.request.GET.getlist('brands'):
            queryset = queryset.filter(brand__id__in=brands)

        if (price_filter_param := self.request.GET.get('price')) is not None:
            parsed_prices = re.findall(r'\$\d{1,4}', price_filter_param)
            if len(parsed_prices) == 2:
                min_price, max_price = (Decimal(price[1:]) for price in parsed_prices)
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset
