from django_filters import rest_framework as filters

from .models import Title, Genre, Category


class GenreFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name="genre__slug", method='filter_genre')
    category = filters.CharFilter(
        field_name="category__slug",
        method='filter_cat'
    )
    year = filters.CharFilter(field_name="year", lookup_expr='iexact')
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']

    def filter_genre(self, queryset, slug, genre):
        return queryset.filter(genre__slug__contains=genre)

    def filter_cat(self, queryset, slug, category):
        return queryset.filter(category__slug__contains=category)
