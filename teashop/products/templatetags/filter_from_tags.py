from django import template
from django.http import QueryDict

register = template.Library()


@register.filter(name='get_list_from_query_dict')
def get_list_from_query_dict(query_dict: QueryDict, key: int | str) -> list:
    """
        Функция возвращает список оп ключу из query_dict,
        если ключа нет, возвращает пустой список.
    """
    query_list = query_dict.getlist(key)
    return query_list if query_list is not None else []


@register.filter(name='convert_to_str')
def convert_to_str(item: int | float) -> str:
    return str(item)
