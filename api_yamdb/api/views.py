from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializerForSafeMethods,
                          TitleSerializerForUnsafeMethods)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def get_object(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return category


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def get_object(self):
        genre = get_object_or_404(Genre, slug=self.kwargs.get('slug'))
        return genre


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=category', '=genre', '=name', 'year')
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action in ('list',):
            return TitleSerializerForSafeMethods
        return TitleSerializerForUnsafeMethods
