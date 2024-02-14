from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .pagination import DefaultPagination
from .models import Collection, OrderItem, Product, Review
from .serializers import ProductSerializer,CollectionSerializer, ReviewSerializer
from django.db.models.aggregates import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=DefaultPagination
    ordering_fields=['unit_price','last_update']
    search_fields=['title','description']

    # def get_queryset(self):
    #     queryset=Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')
    #     print(collection_id)
    #     if collection_id is not None:
    #         queryset=queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'cannot be deleted, associated with order item'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products'))
    serializer_class=CollectionSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        collection=get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=kwargs['pk'])
        if collection.products.count()>0:
            return Response({'error':'collection include one or more product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}




