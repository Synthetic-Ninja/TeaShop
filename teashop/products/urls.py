from django.urls import path

from .views import ProductsListView, ProductFilteredListView

app_name = 'products'


urlpatterns = [
    path('', ProductsListView.as_view(), name='product_list'),
    path('filter/', ProductFilteredListView.as_view(), name='filtered_product_list')
]
