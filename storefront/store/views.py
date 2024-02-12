from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer,CollectionSerializer
from django.db.models.aggregates import Count

# Create your views here.
@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
        queryset=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    # product=Product.objects.get(pk=id)
    product=get_object_or_404(Product,pk=id)

    if request.method=='GET':
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method=='DELETE':
        if product.orderitems.count()>0:
            return Response({'error':'cannot deleted, associted with order item'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])  
def collection_list(request):
    if request.method=='GET':
        queryset=Collection.objects.annotate(products_count=Count('products')).all()
        serializer=CollectionSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    # product=Product.objects.get(pk=id)
    # collection=get_object_or_404(Collection,pk=id)
    # serializer=CollectionSerializer(collection)
    # return Response(serializer.data)
    collection=get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')),pk=pk)
    if request.method=="GET":
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=="DELETE":
        if collection.products.count()>0:
            return Response({'error':'collection include one or more product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



