from django.urls import path
from . import views
from pprint import pprint
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('carts',views.CartViewSet)
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('customers',views.CustomerViewSet)

# pprint(router.urls)

products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

carts_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items')

urlpatterns =router.urls+products_router.urls+carts_router.urls