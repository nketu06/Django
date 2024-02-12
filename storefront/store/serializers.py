from decimal import Decimal
from rest_framework import serializers
from .models import Collection, Product

# class CollectionSerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     title=serializers.CharField(max_length=255)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count']
    products_count=serializers.IntegerField()
        

# class ProductSerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     title=serializers.CharField(max_length=255)
#     price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
#     price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
#     collection=serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self,product):
        return product.unit_price*Decimal(1.1)
    
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError("password do not match")
    #     return data