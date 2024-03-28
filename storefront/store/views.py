from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .pagination import DefaultPagination
from .models import Cart, CartItem, Collection, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, ProductSerializer,CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
from django.db.models.aggregates import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,GenericViewSet
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
    
class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        if self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')




