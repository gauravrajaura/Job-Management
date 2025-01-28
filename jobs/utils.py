from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = (
        "page_size"  # Allows the client to specify page size in the query params
    )
    max_page_size = 100
