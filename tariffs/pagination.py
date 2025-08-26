from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_query_param = "page"
    page_size_query_param = "page_size"   # клиент может управлять размером страницы
    max_page_size = 100                   # безопасный верхний предел

class DefaultLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 100
