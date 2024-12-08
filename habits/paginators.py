from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """Пагинатор страниц для модели Habit"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
