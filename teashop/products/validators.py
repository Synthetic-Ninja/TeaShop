import re

from django.http import QueryDict

class FilterValidator:
    """Класс валидатора, проверяет на валидность входящие get параметры для фильтрации"""

    def __init__(self, get_params: QueryDict):
        self.params = get_params

    def __check_price(self) -> bool:
        """Функция проверяет, что в параметре цены действительно два числа"""

        parsed_price = re.findall(r'\$\d{1,4}', self.params.get('price'))
        if parsed_price is not None:
            return len(parsed_price) == 2
        return False

    def __check_brands(self) -> bool:
        """Функция проверяет, что все объекты списка параметров brands являются числами"""

        return all([item.isdigit() for item in self.params.getlist('brands')])

    def __check_category(self) -> bool:
        """Функция проверят, что параметр категория действительно число"""

        return self.params.get('category').isdigit()


    def is_valid(self) -> bool:
        """
        Общая функция проверки входящий параметров, проверяет какие ключи находятся в
        в get параметрах и исходя из этого запускает проверки на валидность этих параметров
        """
        if self.params.get('brands') is not None:
            if not self.__check_brands():
                return False

        if self.params.get('price') is not None:
            if not self.__check_price():
                return False

        if self.params.get('category') is not None:
            if not self.__check_category():
                return False

        return True

