from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, viewsets, status, filters
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from api.users.permissions import (
    IsAdminPermission,
    IsModeratorPermission,
    IsOwnerPermission
)

from .filters import GenreFilter
from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    filterset_class = GenreFilter

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_object(self):
        try:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, **filter_kwargs)
        except Http404:
            if self.request.method in ['DELETE', 'GET', 'PATCH']:
                raise MethodNotAllowed(self.request.method)
            raise Http404
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]


class GenreViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_object(self):
        try:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, **filter_kwargs)
        except Http404:
            if self.request.method in ['DELETE', 'GET', 'PATCH']:
                raise MethodNotAllowed(self.request.method)
            raise Http404
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]
