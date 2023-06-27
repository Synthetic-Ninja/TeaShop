from django.test import TestCase
from django.http import QueryDict
from django.urls import reverse

from .validators import FilterValidator


class ValidatorTestCase(TestCase):
    validator = FilterValidator

    def __base_validator_test(self, get_params, reference):
        """Базовая функция тестирования создает объект QueryDict из параметра get_params
           и проводит проверку на соответствие с переданным параметром reference"""

        get_params = QueryDict(get_params, mutable=True)
        result = self.validator(get_params).is_valid()
        self.assertEqual(result, reference)

    # ____________________Тесты парaметра цена____________________________
    def test_valid_price_with_special_symbols(self):
        self.__base_validator_test('price=%240+-+%24120', True)

    def test_valid_price_without_special_symbols(self):
        self.__base_validator_test('price=240+-+24120', True)

    def test_price_without_digits(self):
        self.__base_validator_test('price=aaa+-+aaa', False)

    def test_price_with_more_digits(self):
        self.__base_validator_test(f'price={"1" * 10}+-+{"2" * 10}', False)

    # ____________________Тесты параметра бренд____________________________

    def test_one_brand(self):
        self.__base_validator_test('brands=1', True)

    def test_many_brand(self):
        self.__base_validator_test('brands=1&brands=2&brands=3', True)

    def test_invalid_single_brand_param(self):
        self.__base_validator_test('brands=a', False)

    def test_invalid_multi_brand_param(self):
        self.__base_validator_test('brands=a&brands=a&brands=a', False)

    def test_invalid_multi_brand_param_mixed(self):
        self.__base_validator_test('brands=1&brands=a&brands=2', False)

    # ____________________Тесты параметра категория____________________________
    def test_valid_category_param(self):
        self.__base_validator_test('category=2', True)

    def test_invalid_category_param(self):
        self.__base_validator_test('category=a', False)


class ProductListViewTestCase(TestCase):
    path = reverse('products:product_list')

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
